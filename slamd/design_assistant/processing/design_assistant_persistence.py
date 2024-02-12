from flask import session 


class DesignAssistantPersistence:

    

    @classmethod
    def set_session_interaction_step(cls):
        current_interaction_step = cls.get_session_property('interaction_step')
        if (current_interaction_step > 0):
            session['interaction_step'] = current_interaction_step + 1
        else:    
            session['interaction_step'] = 1 

    @classmethod
    def get_session_property(cls, property):
        return session.get(property, 0)

    @classmethod
    def set_session_task(cls, task):
        session['task'] = task

