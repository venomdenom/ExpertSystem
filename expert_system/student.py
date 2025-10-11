from expert_system.base import BaseExpertSystem


class StudentExpertSystem(BaseExpertSystem):
    """Student admission expert system - domain-specific implementation."""

    def __init__(self):
        super().__init__()
        self.results = {
            'admission_probability': 0,
            'recommendations': [],
            'status': 'N/A'
        }

    def _setup_custom_evaluators(self):
        """Register student-specific evaluators if needed."""
        pass

    def _setup_custom_actions(self):
        """Register student-specific action handlers."""
        self.action_registry.register('set_result', self._handle_set_result)
        self.action_registry.register('add_recommendation',
                                      self._handle_add_recommendation)
        self.action_registry.register('update_probability',
                                      self._handle_update_probability)

    def _handle_set_result(self, probability: int, status: str,
                           recommendation: str):
        """Handler for set_result action."""
        self.results['admission_probability'] = probability
        self.results['status'] = status
        self.results['recommendations'].append(recommendation)

    def _handle_add_recommendation(
            self,
            recommendation: str,
            probability: int = None,
            status: str = None
    ):
        """Handler for add_recommendation action."""
        if probability and probability > self.results['admission_probability']:
            self.results['admission_probability'] = probability
        if status and self.results['status'] == 'N/A':
            self.results['status'] = status
        self.results['recommendations'].append(recommendation)

    def _handle_update_probability(self, delta: int):
        """Handler for updating probability by delta."""
        self.results['admission_probability'] = max(
            0,
            min(100, self.results['admission_probability'] + delta)
        )
