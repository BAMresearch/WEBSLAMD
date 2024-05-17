import {assignClickEventToSubmitButton} from "./utils.js";
import {assignClickEventToTaskForm} from "./task.js"
import {assignClickEventToMaterialTypeField} from "./material_type.js";
import { assignClickEventToDesignTargetForm, handleDesignTargetsSubmission, handleAddingCustomDesignTarget} from "./zero_shot_learner/design_targets.js";
import { assignEventsToTargetValuesForm} from "./zero_shot_learner/design_targets_values.js";
import {assignClickEventToPowdersForm, handlePowdersSubmission} from "./zero_shot_learner/powder.js";
import {assignClickEventToLiquidForm, handleAddingLiquid, handleLiquidSubmission} from "./zero_shot_learner/liquid.js";
import {assignClickEventToOtherForm, handleAddingOther, handleOtherSubmission} from "./zero_shot_learner/other.js";
import {assignInputEventToCommentForm, handleCommentSubmission} from "./zero_shot_learner/comment.js";
import {handleDeleteDesignAssistantSession} from "./design_assistant_session.js"
import { assignEventsToDesignKnowledgeForm } from "./zero_shot_learner/design_knowledge.js"
import { assignEventsToNamePowderStep } from "./data_creation/powder_name.js";
import { assignEventsToCostsPowderStep } from './data_creation/powder_costs.js'
import { assignEventsToOxideCompositionPowderStep } from './data_creation/powder_oxide_composition.js'
import { assignEventsToStructuralCompositionPowderStep } from "./data_creation/powder_structural_composition.js";
import { assignEventsToNameLiquidStep } from "./data_creation/liquid_name.js";
import { assignEventsToCostsLiquidStep } from "./data_creation/liquid_costs.js";
import { assignEventsToOxideCompositionLiquidStep } from "./data_creation/liquid_oxide_composition.js";
import { assignEventsToNameAggregateStep } from "./data_creation/aggregate_name.js";
import { assignEventsToCostsAggregateStep } from "./data_creation/aggregate_costs.js";
import { assignEventsToCompositionAggregateStep } from "./data_creation/aggregate_composition.js";
import { assignEventsToNameAdmixtureStep } from "./data_creation/admixture_name.js";
import { assignEventsToCostsAdmixtureStep } from "./data_creation/admixture_costs.js";
import { assignEventsToNameProcessStep } from "./data_creation/process_name.js";
import { assignEventsToCostsProcessStep } from "./data_creation/process_costs.js";
import { assignEventsToInformationProcessStep } from "./data_creation/process_information.js";
import { assignEventsToFormulationStep } from './data_creation/formulation.js'

window.addEventListener("load", function () {
    document.getElementById("nav-bar-design-assistant").setAttribute("class", "nav-link active");
    assignClickEventToSubmitButton("delete_session_button", handleDeleteDesignAssistantSession);
    assignClickEventToTaskForm();
    assignClickEventToMaterialTypeField();
    assignClickEventToSubmitButton("design_targets_submit_button", handleDesignTargetsSubmission);
    assignClickEventToSubmitButton("powders_submit_button", handlePowdersSubmission);
    assignClickEventToDesignTargetForm();
    assignClickEventToPowdersForm();
    assignClickEventToSubmitButton("additional_design_targets_button", handleAddingCustomDesignTarget);
    assignClickEventToSubmitButton("submit_liquid_button", handleLiquidSubmission);
    assignClickEventToSubmitButton("additional_liquid_button", handleAddingLiquid);
    assignClickEventToLiquidForm();
    assignClickEventToSubmitButton("submit_other_button", handleOtherSubmission);
    assignClickEventToSubmitButton("additional_other_button", handleAddingOther);
    assignClickEventToOtherForm();
    assignClickEventToSubmitButton("submit_comment_button", handleCommentSubmission);
    assignInputEventToCommentForm()
    assignEventsToDesignKnowledgeForm()
    assignEventsToTargetValuesForm()
    assignEventsToNamePowderStep()
    assignEventsToCostsPowderStep() 
    assignEventsToOxideCompositionPowderStep()
    assignEventsToStructuralCompositionPowderStep()
    assignEventsToNameLiquidStep()
    assignEventsToCostsLiquidStep()
    assignEventsToOxideCompositionLiquidStep()
    assignEventsToNameAggregateStep()
    assignEventsToCostsAggregateStep()
    assignEventsToCompositionAggregateStep()
    assignEventsToNameAdmixtureStep()
    assignEventsToCostsAdmixtureStep()
    assignEventsToNameProcessStep()
    assignEventsToCostsProcessStep()
    assignEventsToInformationProcessStep()
    assignEventsToFormulationStep()
});