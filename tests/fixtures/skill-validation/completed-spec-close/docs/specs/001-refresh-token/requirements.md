# Requirements

## Requirements

### Requirement 1: Refresh Token Rotation

**User Story:** As an operator, I want refresh tokens to rotate, so that stale
tokens cannot be reused.

#### Acceptance Criteria

1. GIVEN a refresh request, WHEN a token is accepted, THEN THE SYSTEM SHALL
   issue a replacement token.
