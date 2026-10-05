from __future__ import annotations


def select_covariates(available_covariates: list[str], requested_covariates: list[str] | None = None) -> list[str]:
    requested = requested_covariates or []
    return [covariate for covariate in requested if covariate in set(available_covariates)]
