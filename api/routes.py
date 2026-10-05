from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from core.algorithm_registry import get_all_algorithms, get_algorithm
from core.execution_engine import ExecutionEngine, ALGORITHM_MAP
from analysis.benchmark import run_benchmark_series
from input.generators import generate_input_for_algorithm
from api.schemas import (
    CompareRequest, GenerateRequest, RunRequest,
    APIErrorResponse, APIErrorPayload
)

router = APIRouter(prefix="/api")
engine = ExecutionEngine()


@router.get("/algorithms")
def list_algorithms():
    return [alg.model_dump() for alg in get_all_algorithms()]


@router.post("/generate")
def generate_input(req: GenerateRequest):
    meta = get_algorithm(req.algorithm_id)
    if not meta:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=APIErrorResponse(
                error=APIErrorPayload(
                    code="INVALID_ALGORITHM",
                    message=f"Algorithm '{req.algorithm_id}' not found."
                )
            ).model_dump()
        )

    # Check preset
    if req.preset_name:
        for preset in meta.presets:
            if preset.name == req.preset_name:
                return {"input": preset.input}

    # Generate random
    kind = meta.input_schema.kind
    generated = generate_input_for_algorithm(kind, req.size, input_type=req.input_type or "random")
    return {"input": generated}


@router.post("/run")
def run_algorithm(req: RunRequest):
    try:
        result = engine.execute(req.algorithm_id, req.input)
        return result.model_dump()
    except ValueError as val_err:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=APIErrorResponse(
                error=APIErrorPayload(
                    code="VALIDATION_ERROR",
                    message=str(val_err)
                )
            ).model_dump()
        )
    except Exception as err:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=APIErrorResponse(
                error=APIErrorPayload(
                    code="EXECUTION_ERROR",
                    message=str(err)
                )
            ).model_dump()
        )


@router.post("/compare")
def compare_algorithms(req: CompareRequest):
    try:
        if not req.algorithm_ids:
            raise ValueError("No algorithms selected for comparison.")

        first_meta = get_algorithm(req.algorithm_ids[0])
        schema_kind = first_meta.input_schema.kind if first_meta else "array"

        def benchmark_generator(kind, size, rand_inst):
            return generate_input_for_algorithm(schema_kind, size, rand_inst, input_type=req.input_kind)

        def make_silent_runner(alg_id):
            alg_func = ALGORITHM_MAP.get(alg_id)
            if not alg_func:
                return None
            return lambda inp, mode="silent", fn=alg_func: fn(inp, mode="silent")

        runners = {alg_id: make_silent_runner(alg_id) for alg_id in req.algorithm_ids if make_silent_runner(alg_id)}

        resp = run_benchmark_series(
            algorithm_ids=req.algorithm_ids,
            input_kind=req.group,
            sizes=req.sizes,
            repeats=req.repeats,
            seed=req.seed,
            alg_runners=runners,
            generator_func=benchmark_generator
        )
        return resp.model_dump()
    except Exception as err:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=APIErrorResponse(
                error=APIErrorPayload(
                    code="COMPARE_ERROR",
                    message=str(err)
                )
            ).model_dump()
        )
