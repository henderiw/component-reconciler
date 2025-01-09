from pydantic import ValidationError
import json 
import reconciler
from topology_types import Topology
#from  user import User
from reconciler.imports import retrieve

class Reconciler(reconciler.Reconciler):
  def reconcile(self, object: str) -> reconciler.ReconcileResult:
    # Example values for the result
    requeue = False  # Whether to requeue
    requeue_after = 30  # Requeue after 30 seconds  

    x = retrieve.get("wim")
    print(x)

    try:
      # Parse the JSON string into a dictionary
      topo_data = json.loads(object)
      
      # Pass the parsed data to the Topology model
      topo = Topology(**topo_data)
      #print(topo_data)
      nodes = topo.construct_nodes()
      links = topo.construct_links()

    except json.JSONDecodeError as e:
      # Handle JSON parsing errors
      raise reconciler.types.Err(reconciler.ReconcileError(
          code=1,
          message=f"Invalid JSON: {str(e)}"
      ))
    except ValidationError as e:
      raise reconciler.types.Err(reconciler.ReconcileError(
          code=2,
          message=f"valiation error: {str(e)}"
      ))
    except Exception as e:
      # Handle other errors, such as validation errors
      raise reconciler.types.Err(reconciler.ReconcileError(
          code=0,
          message=str(e)
      ))
    
    # Return the result with appropriate values
    return reconciler.ReconcileResult(
        requeue=requeue,
        requeue_after=requeue_after,
        object=f"Constructed: {links}"
    )
