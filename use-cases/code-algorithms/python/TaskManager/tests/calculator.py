def calculate_compound_interest(
    principal_amount,
    annual_interest_rate,
    time_years,
    additional_amount=0,
    compounding_frequency_per_year=12
):
    accumulated_amount = principal_amount

    interest_rate_per_period = annual_interest_rate / 100 / compounding_frequency_per_year
    total_periods = time_years * compounding_frequency_per_year

    for period_index in range(1, total_periods + 1):
        periodic_interest = accumulated_amount * interest_rate_per_period
        accumulated_amount += periodic_interest

        is_year_end = period_index % compounding_frequency_per_year == 0
        is_not_final_period = period_index < total_periods

        if is_year_end and is_not_final_period:
            accumulated_amount += additional_amount

    return {
        "final_amount": round(accumulated_amount, 2),
        "interest_earned": round(
            accumulated_amount
            - principal_amount
            - (additional_amount * (time_years - 1)),
            2
        ),
        "total_contributions": principal_amount + (additional_amount * (time_years - 1))
    }
