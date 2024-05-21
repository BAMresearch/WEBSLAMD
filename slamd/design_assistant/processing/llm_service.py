import openai
import os

from slamd.common.error_handling import FreeTrialLimitExhaustedException, ValueNotSupportedException, \
    LLMNotRespondingException
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence

MAX_FREE_LLM_CALLS = 10
MODEL = 'gpt-3.5-turbo'


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
    def generate_design_knowledge(cls, token):
        prompt = cls._generate_design_knowledge_prompt()
        user_message = {"role": "user", "content": prompt}
        generated_design_knowledge = cls._generate_openai_llm_response([user_message], MODEL, token)
        return generated_design_knowledge

    @classmethod
    def _generate_design_knowledge_prompt(cls):
        # load session data to construct prompt excerpts       
        design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
        zero_shot_learner_session = design_assistant_session['zero_shot_learner']
        # generate user excerpt
        user_input_excerpt = cls._generate_design_knowledge_user_input_excerpt(zero_shot_learner_session)
        # generate instruction excerpt
        instruction_excerpt = cls._generate_design_knowledge_instruction_excerpt(zero_shot_learner_session)
        # combine user excerpt with system excerpt and instruction excerpt to build final design knowledge prompt
        design_knowledge_prompt = instruction_excerpt + user_input_excerpt
        print(design_knowledge_prompt)
        return design_knowledge_prompt

    @classmethod
    def _generate_design_knowledge_design_targets_system_excerpt(cls, zero_shot_learner_session):
        design_targets = zero_shot_learner_session["design_targets"]
        design_targets_system_excerpt, design_target_optimization = '', ''
        if len(design_targets) == 1:
            design_targets_system_excerpt = " the design"
        else:
            for idx, design_target in enumerate(design_targets):
                excerpt_and = ''
                if design_target["design_target_optimization_field"] == 'decrease':
                    design_target_optimization = 'minimizing the '
                if design_target["design_target_optimization_field"] == 'increase':
                    design_target_optimization = 'maximizing the '
                if design_target["design_target_optimization_field"] == 'No optimization':
                    design_target_optimization = 'optimizing '
                if (len(design_targets) > 1) and (idx == 0):
                    excerpt_and = ' and '
                design_target_name = design_target["design_target_name_field"]
                design_targets_system_excerpt += design_target_optimization + design_target_name + excerpt_and
            design_targets_system_excerpt += ' during the design'
        return design_targets_system_excerpt

    @classmethod
    def _generate_design_knowledge_instruction_excerpt(cls, zero_shot_learner_session):
        material_type = zero_shot_learner_session['type']
        design_knowledge_design_targets_instruction_excerpt = cls._generate_design_knowledge_design_targets_instruction_excerpt(zero_shot_learner_session)
        instruction_excerpt = (f'You have performed thousands of experiments in the laboratory. You have extensive design proficiency '
                               f'for cementitious materials. You always answer with no more than six crucial sentences captuaring pivotal and '
                               f'quantitative formulation design rules. You always answer in a direct manner, e.g., the change in '
                               f'(parameter) has (effect) due to (influence).'
                               f'Your answer is well-structered in bullet-points. '
                               f'What is the best formulation design knowledge you have for finding {material_type} '
                               f'formulations{design_knowledge_design_targets_instruction_excerpt}?')
        return instruction_excerpt
         
    @classmethod
    def _generate_design_knowledge_design_targets_instruction_excerpt(cls, zero_shot_learner_session):
        design_targets = zero_shot_learner_session["design_targets"]
        design_targets_instruction_excerpt = ', that consist of the specified components and adhere to the specified design targets of '
        design_target_optimization = ''
        for idx, design_target in enumerate(design_targets):
            excerpt_and = ''
            if design_target["design_target_optimization_field"] == 'decrease':
                design_target_optimization = 'minimizing the '
            if design_target["design_target_optimization_field"] == 'increase':
                design_target_optimization = 'maximizing the '
            if design_target["design_target_optimization_field"] == 'No optimization':
                design_target_optimization = 'optimizing '
            if len(design_targets) > 1 and idx == 0:
                excerpt_and = ' and '
            design_target_name = design_target["design_target_name_field"]
            design_targets_instruction_excerpt += design_target_optimization + design_target_name + excerpt_and
        return design_targets_instruction_excerpt
    
    @classmethod
    def _generate_design_knowledge_user_input_excerpt(cls, zero_shot_learner_session):
        material_type_excerpt = cls._generate_material_type_user_input_excerpt(zero_shot_learner_session)
        powders_excerpt = cls._generate_powders_user_input_excerpt(zero_shot_learner_session)
        liquid_excerpt = cls._generate_liquids_user_input_excerpt(zero_shot_learner_session)
        other_excerpt = cls._generate_other_user_input_excerpt(zero_shot_learner_session)
        comment_excerpt = cls._generate_comment_user_input_excerpt(zero_shot_learner_session)
        design_targets_excerpt = cls._generate_design_targets_user_input_excerpt(zero_shot_learner_session)
        user_input_excerpt = material_type_excerpt + '////Components: \n' + powders_excerpt + liquid_excerpt + other_excerpt + comment_excerpt + design_targets_excerpt
        return user_input_excerpt

    @classmethod
    def _generate_material_type_user_input_excerpt(cls, zero_shot_learner_session):
        material_type = zero_shot_learner_session['type']
        material_type_prompt_excerpt = f'You want to design {material_type.capitalize()} formulations that consist of the following components: \n'
        return material_type_prompt_excerpt

    @classmethod
    def _generate_powders_user_input_excerpt(cls, zero_shot_learner_session):
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
    def _generate_liquids_user_input_excerpt(cls, zero_shot_learner_session):
        liquid = zero_shot_learner_session['liquids']
        liquid_prompt_excerpt = f'//Liquid : {liquid} \n'
        return liquid_prompt_excerpt

    @classmethod
    def _generate_other_user_input_excerpt(cls, zero_shot_learner_session):
        other = zero_shot_learner_session['other']
        other_prompt_excerpt = ''
        if not other == 'None':
            other_prompt_excerpt = f'//Additional components : {other} \n'
        return other_prompt_excerpt

    @classmethod
    def _generate_comment_user_input_excerpt(cls, zero_shot_learner_session):
        comment = zero_shot_learner_session['comment']
        if comment.strip():
            comment_prompt_excerpt = f'//Additional design information : {comment} \n'
        return comment_prompt_excerpt

    @classmethod
    def _generate_design_targets_user_input_excerpt(cls, zero_shot_learner_session):
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
            design_target_name = design_target["design_target_name_field"]
            design_targets_formatted = design_targets_formatted + '//' + design_target_name + design_target_optimization + design_target_value + '\n'
        design_targets_prompt_excerpt = '////Design Targets: \n' + design_targets_formatted
        return design_targets_prompt_excerpt
    
    @classmethod
    def generate_formulation(cls, design_knowledge, token):
        prompt = cls._generate_zero_shot_learner_prompt(design_knowledge)
        print(prompt)
        user_message = {"role": "user", "content": prompt}
        formulation = cls._generate_openai_llm_response([user_message], MODEL, token)
        return formulation
     
    @classmethod
    def _generate_zero_shot_learner_prompt(cls, design_knowledge):
        design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
        zero_shot_learner_session = design_assistant_session['zero_shot_learner']
        instruction_prompt_excerpt = cls._generate_zero_shot_learner_instruction_excerpt(zero_shot_learner_session)

        output_format_excerpt = cls._create_output_format_excerpt()
        zero_shot_learner_prompt = instruction_prompt_excerpt + '////General design knowledge //' + design_knowledge + "\n " + output_format_excerpt
        return zero_shot_learner_prompt

    @classmethod
    def _generate_zero_shot_learner_instruction_excerpt(cls, zero_shot_learner_session):
        material_type_excerpt = zero_shot_learner_session['type']
        design_targets_excerpt = cls._generate_formulation_design_targets_instruction_excerpt(zero_shot_learner_session)
        instruction_prompt_excerpt = (f"////You are a powerful {material_type_excerpt} formulation prediction model tasked with finding the best "
                                      f"{material_type_excerpt} formulation that {design_targets_excerpt}. You are able to incorporate general design "
                                      f"knowledge to improve your predictions.'\n "
                                      f"Based on the general knowledge, your task is to explicitly give a recipe which lists the ratios or percentages of the "
                                      f"various components involved.\n")

        material_type_excerpt = cls._generate_material_type_user_input_excerpt(zero_shot_learner_session)
        powders_excerpt = cls._generate_powders_user_input_excerpt(zero_shot_learner_session)
        liquid_excerpt = cls._generate_liquids_user_input_excerpt(zero_shot_learner_session)
        other_excerpt = cls._generate_other_user_input_excerpt(zero_shot_learner_session)
        comment_excerpt = cls._generate_comment_user_input_excerpt(zero_shot_learner_session)

        components = material_type_excerpt + powders_excerpt + liquid_excerpt + other_excerpt + comment_excerpt

        instruction_prompt_excerpt += (f"Note that you only want to look for formulations that contain the following components: \n {components}. "
                                       f"In case that you do not want to blend the powders (not blended) it is extremely important to only include one of the powders in your formulation.")
        return instruction_prompt_excerpt
    
    @classmethod
    def _generate_formulation_design_targets_instruction_excerpt(cls, zero_shot_learner_session):
        design_targets = zero_shot_learner_session["design_targets"]
        design_targets_instruction_excerpt, design_target_optimization, design_target_value = '', '', ''
        for idx, design_target in enumerate(design_targets):
            excerpt_and = ''
            if design_target["design_target_optimization_field"] == 'decrease':
                design_target_optimization = 'has a maximum '
            if design_target["design_target_optimization_field"] == 'increase':
                design_target_optimization = 'has a minimum '
            if design_target["design_target_optimization_field"] == 'No optimization':
                design_target_optimization = 'optimizes '
            if len(design_targets) > 1 and idx == 0:
                excerpt_and = ' and '
            design_target_name = design_target["design_target_name_field"]
            design_target_value = ' of ' + design_target["design_target_value_field"]
            design_targets_instruction_excerpt += design_target_optimization + design_target_name + design_target_value + excerpt_and
        return design_targets_instruction_excerpt


    @classmethod
    def _create_output_format_excerpt(cls):
        return """
In your recipe, make sure that the ratios and percentages of the components of all considered materials are consistent.
For examples, if you put out all components in units of percent they must add up to 100%.

All the components of the recipe should be listed in a comma-seperated way. Each component should follow the following pattern.

////
- NAME_OF_THE_COMPONENT: VALUE

For you orientation, here are some examples (note that these are just examples and must not be included in the general knowledge provided; further make sure to use units that are conventional for the components you are proposing):

Example 1:
Water to Cement Ratio: 0.5

Example 2:
Fly Ash: 20%

The full output format thus must look as follows:

NAME_OF_THE_COMPONENT 1: VALUE 1, NAME_OF_THE_COMPONENT 2: VALUE 2, NAME_OF_THE_COMPONENT 3: VALUE 3

and so on until all components are included. Make sure to stick to exactly this format! Here are examples:

Example 1:

Fly Ash: 30%, GGBFS: 70%, Water to Cement Ratio: 0.4

Example 2:

Geopolymer: 30%, Water: 60%, Recycled Aggregates: 10%

Example 3:
Fly Ash: 40%, Water: 25%, Biochar: 10%, Rice Husk Ash: 10%, Recycled Glass Fines: 10%, Super Plasticizer: 5%
"""