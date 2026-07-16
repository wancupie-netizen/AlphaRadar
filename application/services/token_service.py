"""
AlphaRadar Token Service

Application Service responsible for assembling
Token Detail responses.

Responsibilities
----------------
- Collect Core Artifacts.
- Build TokenDetailDTO.
- Remain independent of HTTP.
- Contain no business logic.

The service acts as the bridge between the
Core Intelligence Layer and the Presentation Layer.
"""

from application.mappers.token_mapper import (
    build_token_detail,
)

from core.artifacts.decision_artifact import (
    DecisionArtifact,
)

from core.artifacts.outcome_artifact import (
    OutcomeArtifact,
)

from core.artifacts.learning_artifact import (
    LearningArtifact,
)

from application.dto.token_detail_dto import (
    TokenDetailDTO,
)


class TokenService:
    """
    Application Service for Token Detail.

    This service performs orchestration only.
    """

    def build_token_detail(

        self,

        *,

        header: dict,

        observation: dict,

        signals: list,

        interpretations: list,

        decision: DecisionArtifact,

        outcome: OutcomeArtifact,

        learning: LearningArtifact,

        knowledge: list,

    ) -> TokenDetailDTO:
        """
        Assemble a Token Detail DTO.

        Parameters
        ----------
        header
            Token header information.

        observation
            Observation payload.

        signals
            Signal list.

        interpretations
            Interpretation list.

        decision
            DecisionArtifact.

        outcome
            OutcomeArtifact.

        learning
            LearningArtifact.

        knowledge
            Historical knowledge records.

        Returns
        -------
        TokenDetailDTO
        """

        return build_token_detail(

            header=header,

            observation=observation,

            signals=signals,

            interpretations=interpretations,

            decision=decision,

            outcome=outcome,

            learning=learning,

            knowledge=knowledge,

        )