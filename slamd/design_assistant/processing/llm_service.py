import requests
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence


class LLMService:

    system_prompt = "You have performed thousands of experiments in the laboratory. You have extensive design proficiency in the compressive strength of FA/GGBFS-based geopolymer concrete. You can answer questions succinctly because you know that each question relates to only one part of the big picture. You always answer with no more than 8 concise sentences, each containing quantitative facts and trade-offs that relate only to the compressive strength. You always answer directly, e.g., the change in (parameter) between (lower) and (upper) range has ( effect) due to (influence).  Let’s work this out in a step-by-step way to be sure we have the right answer.";

    @classmethod
    def generate_design_knowledge(cls):
        pass

    @classmethod
    def generate_design_knowledge_prompt(cls):
        request_context = DesignAssistantPersistence.get_session_for_property("zero_shot_learner")

