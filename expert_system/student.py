from typing import List

from expert_system.base import BaseExpertSystem


class StudentExpertSystem(BaseExpertSystem):
    """Expert system for students."""

    def __init__(self):
        super().__init__()
        self.results = {
            'admission_probability': 0,
            'recommendations': [],
            'status': 'N/A'
        }

    def add_facts(self, raw_rules: List[dict[str, float]]):
        # TODO: Timur
        # Ниже идея, факты это просто мапа какая-то
        pass

    def add_rules(self, raw_rules: List[dict]):
        # TODO: Timur
        # Смотри, твоя штука должна уметь читать из файла в какой-то формат,
        # а потом уметь тут распарсить правило в Rule
        # self.add_rule(Rule(
        #     name="Правило 3: Средняя подготовка",
        #     conditions=[
        #         lambda f: 50 <= f.get('assignments', 0) < 60,
        #         lambda f: 50 <= f.get('report', 0) < 70,
        #         lambda f: 40 <= f.get('test', 0) < 60
        #     ],
        #     action=lambda ctx: self._set_result(
        #         ctx, 60, 'Средняя подготовка',
        #         "Средняя подготовка."
        #         " Рекомендуется улучшить все показатели."
        #     ),
        #     priority=8
        # ))
        pass

    @staticmethod
    def _set_result(ctx, probability, status, recommendation):
        ctx.results['admission_probability'] = probability
        ctx.results['status'] = status
        ctx.results['recommendations'].append(recommendation)

    @staticmethod
    def _add_recommendation(ctx, probability, status, recommendation):
        if probability and probability > ctx.results['admission_probability']:
            ctx.results['admission_probability'] = probability
        if status and ctx.results['status'] == 'Не определен':
            ctx.results['status'] = status
        ctx.results['recommendations'].append(recommendation)
