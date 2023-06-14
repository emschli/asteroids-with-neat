import pickle


def getNameOfBestNetEver(path):
    complete_path = path + "stats"
    stats = pickle.load(open(complete_path, "rb"))

    fitness = [c.fitness for c in stats.most_fit_genomes]

    generation_of_best_fitness_ever = fitness.index(max(fitness))
    return "{}.net".format(generation_of_best_fitness_ever)


if __name__ == "__main__":
    from get_project_root import root_path

    BASE_PATH = root_path(ignore_cwd=True) + "/resources/trainingResults/"
    RUN_FOLDER = "v2_best/"

    COMPLETE_PATH = BASE_PATH + RUN_FOLDER + "stats"
    statistics = pickle.load(open(COMPLETE_PATH, "rb"))
