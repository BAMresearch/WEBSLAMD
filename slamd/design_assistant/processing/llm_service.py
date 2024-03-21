import requests
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence


class LLMService:

    system_prompt = "You have performed thousands of experiments in the laboratory. You have extensive design proficiency in the compressive strength of FA/GGBFS-based geopolymer concrete. You can answer questions succinctly because you know that each question relates to only one part of the big picture. You always answer with no more than 8 concise sentences, each containing quantitative facts and trade-offs that relate only to the compressive strength. You always answer directly, e.g., the change in (parameter) between (lower) and (upper) range has ( effect) due to (influence).  Let’s work this out in a step-by-step way to be sure we have the right answer. \n";

    user_prompt = ''

    @classmethod
    def generate_design_knowledge(cls):
        prompt = cls._generate_design_knowledge_prompt()

    @classmethod
    def _generate_design_knowledge_prompt(cls):
        design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
        design_assistant_session = design_assistant_session['zero_shot_learner']
        material_type = design_assistant_session['type']
        powders = design_assistant_session['powders']['selected']
        blend_powders = design_assistant_session['powders']['blend']
        liquid = design_assistant_session['liquid']
        other = design_assistant_session['other']
        comment = design_assistant_session['comment']
        user_prompt = ''
        material_type_prompt_excerpt = f'What is the best design knowledge you have for finding {material_type.lower()} formulations with the highest possible compressive strength consisting of the following parameters: \n'
        user_prompt += material_type_prompt_excerpt
        if len(powders) > 1:
            powders = ', '.join(powders)
            if blend_powders == 'yes':
                powders = f'blend of {powders}'
            else:
                powders = f'{powders}, not blended'
        powders_prompt_excerpt = f'Powders : {powders} \n'
        user_prompt += powders_prompt_excerpt
        liquid_prompt_excerpt = f'Liquid : {liquid} \n'
        user_prompt += liquid_prompt_excerpt
        if other:
            other_prompt_excerpt = f'Other components : {other} \n'
            user_prompt += other_prompt_excerpt
        if comment:
            comment_prompt_excerpt = f'Additional comments : {comment} \n'
            user_prompt += comment_prompt_excerpt
        design_targets = design_assistant_session['design_targets']
        design_targets_formatted = ''
        design_target_optimization = ''
        for idx, design_target in enumerate(design_targets):
            if design_target["design_target_optimization_field"] == 'minimized':
                design_target_optimization = 'a maximum of'
            if design_target["design_target_optimization_field"] == 'maximized':
                design_target_optimization = 'at least'
            design_targets_formatted = design_targets_formatted + f'{design_target["design_target_name_field"].capitalize()} with ' + design_target_optimization + f'design_target["design_target_value_field"] \n'
        design_targets_prompt_excerpt = "The following design targets need to be optimized:\n" + design_targets_formatted
        user_prompt += design_targets_prompt_excerpt
        prompt = cls.system_prompt + user_prompt

        return prompt

    # @classmethod
    # def send





