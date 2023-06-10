import neat.reporting


class ReporterForRandomness(neat.reporting.BaseReporter):

    def __init__(self, evaluator):
        self.evaluator = evaluator

    def end_generation(self, config, population, species_set):
        print("Resetting Seeds of Evaluator")
        self.evaluator.generateSeeds()
