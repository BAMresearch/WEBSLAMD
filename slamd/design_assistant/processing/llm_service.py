import requests
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence


class LLMService:

    system_prompt = "You have performed thousands of experiments in the laboratory. You have extensive design proficiency in the compressive strength of FA/GGBFS-based geopolymer concrete. You can answer questions succinctly because you know that each question relates to only one part of the big picture. You always answer with no more than 8 concise sentences, each containing quantitative facts and trade-offs that relate only to the compressive strength. You always answer directly, e.g., the change in (parameter) between (lower) and (upper) range has ( effect) due to (influence).  Let’s work this out in a step-by-step way to be sure we have the right answer.";

    user_prompt = ''

    @classmethod
    def generate_design_knowledge(cls):
        cls._generate_design_knowledge_prompt()

    @classmethod
    def _generate_design_knowledge_prompt(cls):
        design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
        print('request context from session: ', design_assistant_session)
        material_type = design_assistant_session['type']
        powders = design_assistant_session['powders']['selected']
        blend_powders = design_assistant_session['powders']['blend']
        liquid = design_assistant_session['liquid']
        other = design_assistant_session['other']
        comment = design_assistant_session['comment']
        design_targets = design_assistant_session['design_targets']
        user_prompt = ''
        material_type_prompt_excerpt = f'What is the best design knowledge you have for finding ${material_type} formulations with the highest possible compressive strength consisting of the following parameters: \n'
        user_prompt = user_prompt + material_type_prompt_excerpt
        design_targets_formatted = ''
        for design_target in design_targets:
            design_targets_formatted = design_targets_formatted + ''
        if len(powders) > 1:
            powders = ', '.join(powders)
            if blend_powders == 'yes':
                powders = f'blend of ${powders}'
            else:
                powders = f'${powders}, not blended'
        powders_prompt_excerpt = f'Powders : ${powders} \n'
        user_prompt = user_prompt + powders_prompt_excerpt
        liquid_prompt_excerpt = f'Liquid : ${liquid} \n'
        user_prompt = user_prompt + liquid_prompt_excerpt
        if other:
            other_prompt_excerpt = f'Other components : ${other} \n'
            user_prompt = user_prompt + other_prompt_excerpt





