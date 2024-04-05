import openai
import os

from slamd.common.error_handling import FreeTrialLimitExhaustedException, ValueNotSupportedException, \
    LLMNotRespondingException
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence

MAX_FREE_LLM_CALLS = 10
MODELNAME = 'gpt-3.5-turbo'

class LLMService:

    @classmethod
    def _generate_openai_llm_response(cls, messages, model, token):
        if token:
            api_key = token
        else:
            api_key = cls.use_free_tier_token()
        client = openai.OpenAI(api_key=api_key)
        try:
            model_response = client.chat.completions.create(
                messages=messages,
                model=model
            )
            return model_response.choices[0].message.content
        except openai.AuthenticationError:
            raise ValueNotSupportedException('Invalid Token. Generate one from OpenAI.')
        except Exception:
            raise LLMNotRespondingException('LLM is currently not available.')

    @classmethod
    def use_free_tier_token(cls):
        count = DesignAssistantPersistence.get_free_llm_calls_count()
        if count < MAX_FREE_LLM_CALLS:
            token = os.getenv('OPENAI_API_TOKEN')
            DesignAssistantPersistence.update_remaining_free_llm_calls()
            return token
        else:
            raise FreeTrialLimitExhaustedException('Please provide your token.')
        
    @classmethod
    def generate_formulation(cls, design_knowledge, token):
        prompt = cls._generate_zero_shot_learner_prompt(design_knowledge)
        user_message = {"role": "user", "content": prompt}
        formulation = cls._generate_openai_llm_response([user_message], MODELNAME, token)
        return formulation

    @classmethod
    def generate_design_knowledge(cls, token):
        prompt = cls._generate_design_knowledge_prompt()
        user_message = {"role": "user", "content": prompt}
        generated_design_knowledge = cls._generate_openai_llm_response([user_message], MODELNAME, token)
        return generated_design_knowledge
    
    @classmethod
    def _generate_zero_shot_learner_prompt(cls, design_knowledge):
        design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
        zero_shot_learner_session = design_assistant_session['zero_shot_learner']
        instruction_prompt_excerpt = cls._generate_zero_shot_learner_instruction_excerpt(zero_shot_learner_session)
        zero_shot_learner_prompt = instruction_prompt_excerpt + '////General design knowledge //' + design_knowledge
        return zero_shot_learner_prompt

    @classmethod
    def _generate_design_knowledge_prompt(cls):
        # load session data to construct prompt
        design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
        zero_shot_learner_session = design_assistant_session['zero_shot_learner']
        # generate prompt excerpts and combine them to user prompt
        material_type_excerpt = cls._generate_material_type_excerpt(zero_shot_learner_session)
        powders_excerpt = cls._generate_powders_excerpt(zero_shot_learner_session)
        liquid_excerpt = cls._generate_liquids_excerpt(zero_shot_learner_session)
        other_excerpt = cls._generate_other_excerpt(zero_shot_learner_session)
        comment_excerpt = cls._generate_comment_excerpt(zero_shot_learner_session)
        design_targets_excerpt = cls._generate_design_targets_excerpt(zero_shot_learner_session)
        user_excerpt = material_type_excerpt + '////Components: \n' + powders_excerpt + liquid_excerpt + other_excerpt + comment_excerpt + design_targets_excerpt
        # combine user prompt with system prompt and instruction to build final prompt
        system_excerpt = cls._generate_design_knowledge_system_excerpt(zero_shot_learner_session)
        material_type = zero_shot_learner_session['type']
        instruction_excerpt = f'What is the best design knowledge you have for finding {material_type} formulations, that consist of the specified components and adhere to the specified design targets?'
        design_knowledge_prompt = system_excerpt + user_excerpt + instruction_excerpt
        return design_knowledge_prompt

    @classmethod
    def _generate_design_knowledge_system_excerpt(cls, zero_shot_learner_session):
        design_targets = zero_shot_learner_session['design_targets']
        design_targets_names = [design_target["design_target_name_field"] for design_target in design_targets]
        if len(design_targets_names) > 1:
            design_targets_names = ' and '.join(design_targets_names)
        system_excerpt =  f"You have performed thousands of experiments in the laboratory. You have extensive design proficiency in the compressive strength of cementitious materials. You can answer questions succinctly because you know that each question relates to only one part of the big picture. You always answer with no more than 8 concise sentences, each containing quantitative facts and trade-offs that relate only to the {design_targets_names}. You always answer directly, e.g., the change in (parameter) between (lower) and (upper) range has (effect) due to (influence).  Let’s work this out in a step-by-step way to be sure we have the right answer. Consider the following scenario:\n";
        return system_excerpt
    
    @classmethod
    def _generate_zero_shot_learner_instruction_excerpt(cls, zero_shot_learner_session):
        material_type_excerpt = zero_shot_learner_session['type']
        powders = zero_shot_learner_session["powders"]['selected']
        powders_blend = zero_shot_learner_session["powders"]['blend']
        powders_excerpt = ''
        if len(powders) > 1:
            if powders_blend == 'Yes':
                powders_excerpt = '/'.join(powders) 
            if powders_blend == 'No':
                powders_excerpt = ', '.join(powders)   
        other = zero_shot_learner_session['other']
        if not other == 'None':
            other_design_space_excerpt = f' //Additional components: {other}'
            other_output_excerpt = f', {other} = {{your estimate}}'
        else:
            other_output_excerpt = ''
            other_design_space_excerpt = ''
        instruction_prompt_excerpt = f"////You are a powerful {material_type_excerpt} formulation prediction model tasked with finding the best {material_type_excerpt} formulation that maximizes compressive strength. Your predictions will be validated in the Laboratory and you will receive the real-world performance. You will learn from the feedback provided to improve your previous suggestions to find a perfect mix design. Make sure that every formulation lies on this parameter grid: //powder content in kg: 360, 370, 380, 390, 400, 410, 420, 430, 440, 450 //water-to-cement (WC) ratio: 0.45, 0.5, 0.55, 0.6 //Materials: {powders_excerpt} at a ratio: 0.7/0.3, 0.6/0.4, 0.5/0.5 //curing: Ambient curing, Heat curing{other_design_space_excerpt}////You are able to incorporate General design knowledge and lab validations to improve your predictions. You can only answer in this exact format with no additional explanations or context: 'The formulation is Powderkg = {{your estimate}}, wc = {{your estimate}}, materials = {{your estimate}}, curing = {{your estimate}} {other_output_excerpt}'\n"
        return instruction_prompt_excerpt

    @classmethod
    def _generate_material_type_excerpt(cls, zero_shot_learner_session):
        material_type = zero_shot_learner_session['type']
        material_type_prompt_excerpt = f'You want to design {material_type.capitalize()} formulations that adhere to the design targets and consist of the following components: \n'
        return material_type_prompt_excerpt

    @classmethod
    def _generate_powders_excerpt(cls, zero_shot_learner_session):
        powders = zero_shot_learner_session['powders']['selected']
        blend_powders = zero_shot_learner_session['powders']['blend']
        powders = ', '.join(powders)
        if blend_powders == 'Yes':
            powders = f'blend of {powders}'
        else:
            powders = f'{powders}, not blended'
        powders_prompt_excerpt = f'//Powders : {powders} \n'
        return powders_prompt_excerpt

    @classmethod
    def _generate_liquids_excerpt(cls, zero_shot_learner_session):
        liquid = zero_shot_learner_session['liquid']
        liquid_prompt_excerpt = f'//Liquid : {liquid} \n'
        return liquid_prompt_excerpt

    @classmethod
    def _generate_other_excerpt(cls, zero_shot_learner_session):
        other = zero_shot_learner_session['other']
        other_prompt_excerpt = ''
        if not other == 'None':
            other_prompt_excerpt = f'//Additional components : {other} \n'
        return other_prompt_excerpt

    @classmethod
    def _generate_comment_excerpt(cls, zero_shot_learner_session):
        comment = zero_shot_learner_session['comment']
        if comment.strip():
            comment_prompt_excerpt = f'//Additional design information : {comment} \n'
        return comment_prompt_excerpt

    @classmethod
    def _generate_design_targets_excerpt(cls, zero_shot_learner_session):
        design_targets = zero_shot_learner_session['design_targets']
        design_targets_formatted = ''
        design_target_optimization = ''
        for idx, design_target in enumerate(design_targets):
            design_target_value = ''
            if design_target["design_target_optimization_field"] == 'decrease':
                design_target_optimization = ' with a maximum of '
            if design_target["design_target_optimization_field"] == 'increase':
                design_target_optimization = ' with at least '
            if design_target["design_target_optimization_field"] == 'No optimization':
                design_target_optimization = ''
            if not design_target["design_target_value_field"] == 'No target value':
                design_target_value = design_target["design_target_value_field"]
            design_targets_formatted = design_targets_formatted + f'//{design_target["design_target_name_field"].capitalize()}' + design_target_optimization + design_target_value + '\n'
        design_targets_prompt_excerpt = '////Design Targets: ' + "The design must optimize for the following design targets:\n" + design_targets_formatted
        return design_targets_prompt_excerpt
