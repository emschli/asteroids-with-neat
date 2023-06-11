import neat.reporting
import pickle


class ReporterForRandomness(neat.reporting.BaseReporter):

    def __init__(self, evaluator, path):
        self.count = 0
        self.path = path
        self.evaluator = evaluator

    def end_generation(self, config, population, species_set):
        print("Resetting Seeds of Evaluator")
        self.evaluator.generateSeeds()

    def post_evaluate(self, config, population, species, best_genome):
        pickle.dump(best_genome, open(self.path + "/" + str(self.count) + ".net", "wb"))
        self.count += 1
