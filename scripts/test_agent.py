
from ai_ops.agent import build_agent


TEST_CASES = [
    {
        "question": "What AI and machine learning skills are listed in my resume?",
        "expected_tools": {"search_resume_documents"},
    },
    {
        "question": "Which product category generated the most revenue?",
        "expected_tools": {"revenue_by_category"},
    },
    {
        "question": (
            "Analyze the business performance using both monthly revenue "
            "and revenue by category. Summarize the monthly trend and "
            "identify which category generated the most revenue."
        ),
        "expected_tools": {"monthly_revenue", "revenue_by_category"},
    },
]


def main():
    agent = build_agent()
    passed = 0

    for index, test_case in enumerate(TEST_CASES, start=1):
        print(f"\n{'=' * 80}")
        print(f"Test {index}: {test_case['question']}")

        try:
            result = agent.invoke({
                "messages": [
                    {"role": "user", "content": test_case["question"]}
                ]
            })

            executed_tools = {
                message.name
                for message in result["messages"]
                if getattr(message, "type", None) == "tool"
            }

            answer = next(
                (
                    message.content
                    for message in reversed(result["messages"])
                    if getattr(message, "type", None) == "ai"
                    and isinstance(message.content, str)
                    and message.content.strip()
                ),
                None,
            )

            missing_tools = test_case["expected_tools"] - executed_tools

            if answer and not missing_tools:
                print("PASS")
                print(f"Tools executed: {sorted(executed_tools)}")
                print(f"Answer: {answer}")
                passed += 1
            else:
                print("FAIL")
                print(f"Expected tools: {sorted(test_case['expected_tools'])}")
                print(f"Actual tools: {sorted(executed_tools)}")
                print(f"Missing tools: {sorted(missing_tools)}")
                print(f"Answer: {answer or 'No text answer returned.'}")

        except Exception as exc:
            print(f"FAIL: {type(exc).__name__}: {exc}")

    print(f"\nEvaluation result: {passed}/{len(TEST_CASES)} passed")

    if passed != len(TEST_CASES):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
