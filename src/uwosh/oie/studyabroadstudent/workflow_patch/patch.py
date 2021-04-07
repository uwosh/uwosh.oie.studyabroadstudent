from Acquisition import aq_inner, aq_parent
from Products.CMFCore.WorkflowCore import ObjectMoved, WorkflowException
from Products.DCWorkflow.events import AfterTransitionEvent, BeforeTransitionEvent
from Products.DCWorkflow.Expression import StateChangeInfo, createExprContext
from Products.DCWorkflow.utils import Message as _
from uwosh.oie.studyabroadstudent.exceptions import StateError
from zope.event import notify


def _executeTransition(self, ob, tdef=None, kwargs=None):
    """
    Private method.
    Puts object in a new state.
    """
    sci = None
    econtext = None
    moved_exc = None
    # Figure out the old and new states.
    old_sdef = self._getWorkflowStateOf(ob)
    old_state = old_sdef.getId()
    if tdef is None:
        new_state = self.initial_state
        former_status = {}
    else:
        new_state = tdef.new_state_id
        if not new_state:
            # Stay in same state.
            new_state = old_state
        former_status = self._getStatusOf(ob)
    new_sdef = self.states.get(new_state, None)
    if new_sdef is None:
        msg = _('Destination state undefined: ${state_id}',
                mapping={'state_id': new_state})
        raise WorkflowException(msg)

    try:
        # Fire "before" event
        notify(BeforeTransitionEvent(ob, self, old_sdef, new_sdef, tdef,
                                     former_status, kwargs))

        # Execute the "before" script.
        if tdef is not None and tdef.script_name:
            script = self.scripts[tdef.script_name]
            # Pass lots of info to the script in a single parameter.
            sci = StateChangeInfo(
                ob, self, former_status, tdef, old_sdef, new_sdef, kwargs)
            try:
                script(sci)  # May throw an exception.
            except ObjectMoved as moved_exc:
                ob = moved_exc.getNewObject()
                # Re-raise after transition
    except StateError as e:
        msg = f'OIE: State Not Changed! {e.message}'
        ob.plone_utils.addPortalMessage(_(msg), type='error')
        return

    # Update variables.
    state_values = new_sdef.var_values
    if state_values is None:
        state_values = {}
    tdef_exprs = None
    if tdef is not None:
        tdef_exprs = tdef.var_exprs
    if tdef_exprs is None:
        tdef_exprs = {}
    status = {}
    for id, vdef in self.variables.items():
        if not vdef.for_status:
            continue
        expr = None
        if id in state_values:
            value = state_values[id]
        elif id in tdef_exprs:
            expr = tdef_exprs[id]
        elif not vdef.update_always and id in former_status:
            # Preserve former value
            value = former_status[id]
        else:
            if vdef.default_expr is not None:
                expr = vdef.default_expr
            else:
                value = vdef.default_value
        if expr is not None:
            # Evaluate an expression.
            if econtext is None:
                # Lazily create the expression context.
                if sci is None:
                    sci = StateChangeInfo(
                        ob, self, former_status, tdef,
                        old_sdef, new_sdef, kwargs)
                econtext = createExprContext(sci)
            value = expr(econtext)
        status[id] = value

    # Update state.
    status[self.state_var] = new_state
    tool = aq_parent(aq_inner(self))
    tool.setStatusOf(self.id, ob, status)

    # Update role to permission assignments.
    self.updateRoleMappingsFor(ob)

    # Execute the "after" script.
    if tdef is not None and tdef.after_script_name:
        script = self.scripts[tdef.after_script_name]
        # Pass lots of info to the script in a single parameter.
        sci = StateChangeInfo(
            ob, self, status, tdef, old_sdef, new_sdef, kwargs)
        script(sci)  # May throw an exception.

    # Fire "after" event
    notify(AfterTransitionEvent(ob, self, old_sdef, new_sdef, tdef, status,
                                kwargs))

    # Return the new state object.
    if moved_exc is not None:
        # Propagate the notification that the object has moved.
        raise moved_exc
    else:
        return new_sdef
