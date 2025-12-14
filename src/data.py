"""Data definitions and preloaded Job-Shop instances."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

# Type aliases for better readability
OperationTuple = Union[Tuple[str, int], Tuple[str, int, str]]
JobSequences = Dict[str, List[OperationTuple]]


@dataclass(frozen=True)
class OperationSpec:
    """Specification of an operation before assigning an identifier."""

    machine: str
    duration: int


@dataclass(frozen=True)
class Operation:
    job_id: str
    op_id: int
    machine: str
    duration: int
    label: str
    setup_time: int = 0  # Time needed to prepare machine for this operation


@dataclass(frozen=True)
class MaintenanceWindow:
    machine: str
    start: int
    duration: int
    label: str = "Maintenance"
    is_recurring: bool = False  # For recurring maintenance
    recurrence_interval: Optional[int] = None  # Repeat every N time units


@dataclass(frozen=True)
class Job:
    job_id: str
    operations: List[Operation]
    priority: int = 3  # 1=critical, 2=high, 3=normal, 4=low
    deadline: Optional[int] = None  # Must finish before this time
    release_time: int = 0  # Can't start before this time


@dataclass(frozen=True)
class JobShopInstance:
    name: str
    jobs: List[Job]
    machines: List[str]
    description: str
    maintenance: List[MaintenanceWindow] = field(default_factory=list)
    created_at: Optional[str] = None  # Timestamp for custom instances
    is_custom: bool = False  # Distinguish user-created from built-in


def _make_instance(
    name: str,
    job_sequences: JobSequences,
    description: str,
    maintenance: Optional[List[MaintenanceWindow]] = None,
) -> JobShopInstance:
    """Expand a dictionary of operation sequences into a full instance.
    
    Args:
        name: Unique identifier for the instance
        job_sequences: Mapping of job IDs to their operation sequences
        description: Human-readable description of the instance
        maintenance: Optional list of maintenance windows
        
    Returns:
        JobShopInstance: Complete instance ready for solving
        
    Raises:
        ValueError: If job_sequences is empty or contains invalid data
    """
    if not job_sequences:
        raise ValueError("job_sequences cannot be empty")
    
    if not name.strip():
        raise ValueError("name cannot be empty")
    jobs: List[Job] = []
    machine_set = set()
    for job_id, ops in job_sequences.items():
        if not ops:
            raise ValueError(f"Job {job_id} has no operations")
        
        operations: List[Operation] = []
        for idx, op in enumerate(ops):
            if len(op) == 3:
                machine, duration, label = op  # type: ignore[misc]
            elif len(op) == 2:
                machine, duration = op  # type: ignore[misc]
                label = f"Etape {idx + 1}"
            else:
                raise ValueError(f"Invalid operation format in job {job_id}: {op}")
            
            if duration <= 0:
                raise ValueError(f"Duration must be positive for {job_id} operation {idx}")
            
            operations.append(
                Operation(
                    job_id=job_id,
                    op_id=idx,
                    machine=machine,
                    duration=duration,
                    label=label,
                )
            )
        jobs.append(Job(job_id=job_id, operations=operations))
        for op in ops:
            machine_set.add(op[0])

    machines = sorted(machine_set)
    return JobShopInstance(
        name=name, jobs=jobs, machines=machines, description=description, maintenance=maintenance or []
    )


def get_instances() -> Dict[str, JobShopInstance]:
    """Provide a dictionary of named, ready-to-use instances."""
    fulfillment = _make_instance(
        name="preparation_commandes",
        job_sequences={
            "Commande e-commerce #A12": [
                ("Station de picking", 3, "Picking rayon"),
                ("Cellule d'emballage", 4, "Emballage carton"),
                ("Imprimante etiquette", 2, "Etiquetage + scan"),
            ],
            "Commande retail #B07": [
                ("Station de picking", 4, "Picking palettes"),
                ("Imprimante etiquette", 1, "Impression BL"),
                ("Cellule d'emballage", 3, "Filmage + scellage"),
            ],
            "Commande express #C21": [
                ("Imprimante etiquette", 2, "Etiquettes prioritaires"),
                ("Station de picking", 2, "Picking rapide"),
                ("Cellule d'emballage", 3, "Mise en caisse"),
            ],
        },
        description="Flux realiste: picking, emballage, etiquetage pour 3 commandes simultanees.",
    )

    fulfillment_maintenance = _make_instance(
        name="preparation_commandes_maintenance",
        job_sequences={
            "Commande e-commerce #A12": [
                ("Station de picking", 3, "Picking rayon"),
                ("Cellule d'emballage", 4, "Emballage carton"),
                ("Imprimante etiquette", 2, "Etiquetage + scan"),
            ],
            "Commande retail #B07": [
                ("Station de picking", 4, "Picking palettes"),
                ("Imprimante etiquette", 1, "Impression BL"),
                ("Cellule d'emballage", 3, "Filmage + scellage"),
            ],
            "Commande express #C21": [
                ("Imprimante etiquette", 2, "Etiquettes prioritaires"),
                ("Station de picking", 2, "Picking rapide"),
                ("Cellule d'emballage", 3, "Mise en caisse"),
            ],
        },
        maintenance=[
            MaintenanceWindow("Cellule d'emballage", start=2, duration=3, label="Maintenance filmage"),
            MaintenanceWindow("Imprimante etiquette", start=6, duration=2, label="Recharge papier"),
        ],
        description="Scenarion avec maintenance planifiee: station d'emballage et imprimante indisponibles sur des fenetres.",
    )

    fulfillment_rush = _make_instance(
        name="preparation_commandes_rush",
        job_sequences={
            "Commande e-commerce #A12": [
                ("Station de picking", 3, "Picking rayon"),
                ("Cellule d'emballage", 4, "Emballage carton"),
                ("Imprimante etiquette", 2, "Etiquetage + scan"),
            ],
            "Commande retail #B07": [
                ("Station de picking", 4, "Picking palettes"),
                ("Imprimante etiquette", 1, "Impression BL"),
                ("Cellule d'emballage", 3, "Filmage + scellage"),
            ],
            "Commande express #C21": [
                ("Imprimante etiquette", 2, "Etiquettes prioritaires"),
                ("Station de picking", 2, "Picking rapide"),
                ("Cellule d'emballage", 3, "Mise en caisse"),
            ],
            "Commande flash #R99": [
                ("Imprimante etiquette", 1, "Etiquette prioritaire"),
                ("Station de picking", 2, "Picking urgence"),
                ("Cellule d'emballage", 2, "Emballage express"),
            ],
        },
        description="Scenario avec commande flash R99 a insérer en urgence dans le flux.",
    )

    didactic = _make_instance(
        name="didactic_3x3",
        job_sequences={
            "Job A": [("M1", 3), ("M2", 2), ("M3", 2)],
            "Job B": [("M2", 2), ("M3", 1), ("M1", 4)],
            "Job C": [("M3", 4), ("M1", 3), ("M2", 1)],
        },
        description="Instance pedagogique: 3 jobs, 3 machines, ordres entrelaces.",
    )

    alternating = _make_instance(
        name="alternating_3x3",
        job_sequences={
            "Job X": [("M1", 2), ("M3", 5), ("M2", 3)],
            "Job Y": [("M2", 4), ("M1", 1), ("M3", 4)],
            "Job Z": [("M3", 3), ("M2", 2), ("M1", 6)],
        },
        description="Instance alternative pour comparer l'effet des ordres machines.",
    )

    return {
        fulfillment.name: fulfillment,
        fulfillment_maintenance.name: fulfillment_maintenance,
        fulfillment_rush.name: fulfillment_rush,
        didactic.name: didactic,
        alternating.name: alternating,
    }


def instance_horizon(instance: JobShopInstance) -> int:
    """Calculate upper bound on the schedule horizon.
    
    The horizon is computed as the maximum of:
    - Sum of all operation and maintenance durations
    - Latest maintenance end time
    
    Args:
        instance: The job shop instance
        
    Returns:
        int: Conservative upper bound for the schedule timeline
    """
    op_sum = sum(op.duration for job in instance.jobs for op in job.operations)
    maint_sum = sum(m.duration for m in instance.maintenance)
    maint_far_end = max((m.start + m.duration for m in instance.maintenance), default=0)
    return max(op_sum + maint_sum, maint_far_end)
