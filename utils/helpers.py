def generate_ai_recommendations(
    health_score,
    failure_probability,
    current_shock,
    current_vibration,
    current_temp,
    current_battery,
):
    recommendations = []

    if health_score < 70:
        recommendations.append(
            "⚠️ Tool health is deteriorating. Schedule maintenance."
        )

    if failure_probability > 40:
        recommendations.append(
            "⚠️ High probability of tool failure."
        )

    if current_shock > 8:
        recommendations.append(
            "• Reduce shock loading by optimizing drilling parameters."
        )

    if current_vibration > 5:
        recommendations.append(
            "• Excessive vibration detected. Review RPM and WOB."
        )

    if current_temp > 85:
        recommendations.append(
            "• Tool temperature is elevated."
        )

    if current_battery < 20:
        recommendations.append(
            "• Battery level is low."
        )

    if not recommendations:
        recommendations.append(
            "✅ Tool condition is healthy. Continue drilling."
        )

    return recommendations