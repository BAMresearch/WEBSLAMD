import openai
import os

from slamd.common.error_handling import FreeTrialLimitExhaustedException, ValueNotSupportedException, \
    LLMNotRespondingException
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence

MAX_FREE_LLM_CALLS = 10


class LLMService:

    @classmethod
    def generate_design_knowledge(cls, token):
        prompt = cls._generate_design_knowledge_prompt()
        user_message = {"role": "user", "content": prompt}
        generated_design_knowledge = cls._generate_openai_llm_response([user_message], 'gpt-3.5-turbo', token)
        return generated_design_knowledge

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
    def _generate_design_knowledge_prompt(cls):
        # load session data to construct prompt
        design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
        zero_shot_learner_session = design_assistant_session['zero_shot_learner']
        # generate prompt excerpts and combine them to user prompt
        material_type_prompt_excerpt = cls._generate_material_type_prompt_excerpt(zero_shot_learner_session)
        powders_prompt_excerpt = cls._generate_powders_prompt_excerpt(zero_shot_learner_session)
        liquid_prompt_excerpt = cls._generate_liquids_prompt_excerpt(zero_shot_learner_session)
        other_prompt_excerpt = cls._generate_other_prompt_excerpt(zero_shot_learner_session)
        comment_prompt_excerpt = cls._generate_comment_prompt_excerpt(zero_shot_learner_session)
        design_targets_prompt_excerpt = cls._generate_design_targets_prompt_excerpt(zero_shot_learner_session)
        user_prompt = material_type_prompt_excerpt + '////Components: \n' + powders_prompt_excerpt + liquid_prompt_excerpt + other_prompt_excerpt + comment_prompt_excerpt + design_targets_prompt_excerpt
        # combine user prompt with system prompt and instruction to build final prompt
        system_prompt = "You have performed thousands of experiments in the laboratory. You have extensive design proficiency in the compressive strength of FA/GGBFS-based geopolymer concrete. You can answer questions succinctly because you know that each question relates to only one part of the big picture. You always answer with no more than 8 concise sentences, each containing quantitative facts and trade-offs that relate only to the compressive strength. You always answer directly, e.g., the change in (parameter) between (lower) and (upper) range has (effect) due to (influence).  Let’s work this out in a step-by-step way to be sure we have the right answer. Consider the following scenario:\n";
        instruction = f'What is the best design knowledge you have for finding concrete formulations, that consist of the specified components, adhere to the specified design targets and have the highest possible compressive strength?'
        prompt = system_prompt + user_prompt + instruction
        return prompt

    @classmethod
    def _generate_material_type_prompt_excerpt(cls, zero_shot_learner_session):
        material_type = zero_shot_learner_session['type']
        material_type_prompt_excerpt = f'You want to design {material_type.capitalize()} formulations with the highest possible compressive strength consisting of the following components: \n'
        return material_type_prompt_excerpt

    @classmethod
    def _generate_powders_prompt_excerpt(cls, zero_shot_learner_session):
        powders = zero_shot_learner_session['powders']['selected']
        blend_powders = zero_shot_learner_session['powders']['blend']
        powders = ', '.join(powders)
        if blend_powders == 'yes':
            powders = f'blend of {powders}'
        else:
            powders = f'{powders}, not blended'
        powders_prompt_excerpt = f'//Powders : {powders} \n'
        return powders_prompt_excerpt

    @classmethod
    def _generate_liquids_prompt_excerpt(cls, zero_shot_learner_session):
        liquid = zero_shot_learner_session['liquid']
        liquid_prompt_excerpt = f'//Liquid : {liquid} \n'
        return liquid_prompt_excerpt

    @classmethod
    def _generate_other_prompt_excerpt(cls, zero_shot_learner_session):
        other = zero_shot_learner_session['other']
        other_prompt_excerpt = ''
        if not other == 'None':
            other_prompt_excerpt = f'//Additional components : {other} \n'
        return other_prompt_excerpt

    @classmethod
    def _generate_comment_prompt_excerpt(cls, zero_shot_learner_session):
        comment = zero_shot_learner_session['comment']
        if comment.strip():
            comment_prompt_excerpt = f'//Additional design information : {comment} \n'
        return comment_prompt_excerpt

    @classmethod
    def _generate_design_targets_prompt_excerpt(cls, zero_shot_learner_session):
        design_targets = zero_shot_learner_session['design_targets']
        design_targets_formatted = ''
        design_target_optimization = ''
        for idx, design_target in enumerate(design_targets):
            if design_target["design_target_optimization_field"] == 'minimized':
                design_target_optimization = ' with a maximum of '
            if design_target["design_target_optimization_field"] == 'maximized':
                design_target_optimization = ' with at least '
            if design_target["design_target_optimization_field"] == 'No optimization':
                design_target_optimization = ''
            if design_target["design_target_value_field"] == 'No target value':
                design_target_value = ''
            if not design_target["design_target_value_field"] == 'No target value':
                design_target_value = design_target["design_target_value_field"]
            design_targets_formatted = design_targets_formatted + f'//{design_target["design_target_name_field"].capitalize()}' + design_target_optimization + design_target_value + '\n'
        design_targets_prompt_excerpt = '////Design Targets: ' + "The design must optimize for the following design targets:\n" + design_targets_formatted
        return design_targets_prompt_excerpt
