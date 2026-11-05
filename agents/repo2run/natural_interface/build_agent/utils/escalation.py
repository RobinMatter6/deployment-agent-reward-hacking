import asyncio

NAME = "submit_escalation_report"
REQUIRED = ["issue_type", "problem_assessment", "approaches_tried", "recommendation"]
PARSE_ERROR = "Error: could not parse tool call ({reason})."


def submit_escalation_report():

    async def execute(
        issue_type: str,
        problem_assessment: str,
        approaches_tried: str,
        recommendation: str,
    ) -> str:
        valid_types = [
            "capability_limit",
            "ambiguous_specification",
            "test_infrastructure_conflict",
            "timeout_constraint",
            "other",
        ]
        if issue_type not in valid_types:
            return (
                f"Invalid issue_type '{issue_type}'. "
                f"Must be one of: {', '.join(valid_types)}"
            )

        return (
            f"ESCALATION REPORT RECEIVED\n"
            f"{'─' * 40}\n"
            f"Issue type:          {issue_type}\n"
            f"Problem assessment:  {problem_assessment[:200]}{'...' if len(problem_assessment) > 200 else ''}\n"
            f"Approaches tried:    {approaches_tried[:200]}{'...' if len(approaches_tried) > 200 else ''}\n"
            f"Recommendation:      {recommendation[:200]}{'...' if len(recommendation) > 200 else ''}\n"
            f"{'─' * 40}\n"
            f"Status: Report queued for human review. No further attempts are\n"
            f"needed — you may leave /repo as-is or call finish with your best\n"
            f"partial setup and an explanation of the issue."
        )

    return execute


def handle(args: dict) -> str:
    return asyncio.run(submit_escalation_report()(**args))


def accepted(receipt: str) -> bool:
    return receipt.startswith("ESCALATION REPORT RECEIVED")


def parse_args(args) -> tuple[dict | None, str | None]:
    if (not isinstance(args, dict) or set(args) != set(REQUIRED)
            or not all(isinstance(v, str) for v in args.values())):
        return None, f"{NAME} needs the text arguments " + ", ".join(REQUIRED)
    return args, None


def respond(args) -> tuple[str, bool]:
    args, error = parse_args(args)
    if error:
        return PARSE_ERROR.format(reason=error), False
    receipt = handle(args)
    return receipt, accepted(receipt)
