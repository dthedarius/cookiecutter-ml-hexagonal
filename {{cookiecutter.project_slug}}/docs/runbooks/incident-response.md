# Runbook: Incident Response

## Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| P1 | Service completely down | 15 minutes |
| P2 | Degraded performance or accuracy | 1 hour |
| P3 | Minor issue, workaround available | 4 hours |

## Common Issues

### Model not loading

**Symptoms**: `/health/ready` returns `not_ready`, predictions fail

**Steps**:
1. Check container logs: `docker compose logs api`
2. Verify model artifacts exist in expected path
3. Check memory usage (model may exceed container limits)
4. Restart service: `docker compose restart api`

### High latency

**Symptoms**: Response time > 500ms

**Steps**:
1. Check CPU/memory usage
2. Review request volume (rate limiting may be needed)
3. Consider scaling horizontally
4. Check if model is being loaded on every request (should be cached)

### Degraded accuracy

**Symptoms**: Prediction quality drops, user complaints

**Steps**:
1. Check recent model deployments
2. Run evaluation on recent data: `make evaluate`
3. Compare against baseline: `make compare`
4. Consider data drift -- check input distribution
5. If needed, rollback to previous model version
