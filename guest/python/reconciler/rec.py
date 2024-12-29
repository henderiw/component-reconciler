import reconciler
#from pydantic import ValidationError
from apis.topo.v1alpha1.topology_types import Topology 

class Reconciler(reconciler.Reconciler):
  def reconcile(self, object: str) -> reconciler.ReconcileResult:
    # Example values for the result
    requeue = False  # Whether to requeue
    requeue_after = 30  # Requeue after 30 seconds
    #response_object = f"Processed: {object}"  # Return a string with processed information

    #try:
    topo = Topology.model_validate(object)
    result = topo.reconcile()
    #except ValidationError as e:
    #  return reconciler.ReconcileError(
    #    code=1,
    #    error=str(e)
    #  )
    
    # Return the result with appropriate values
    return reconciler.ReconcileResult(
        requeue=requeue,
        requeue_after=requeue_after,
        object=result
    )

