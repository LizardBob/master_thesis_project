import json

import environ
import matplotlib.pyplot as plt

env = environ.Env()


class CharGenerator:
    """
    Class which read from file and generates all charts for comparisons.
    File contains object like {'Fetch Students': {'REST Api': 0.123, 'GraphQL Api': 0.123}}
    we pass title, Arrays with values [ ['REST API'], [2.57] ] and [ ['GraphQL API'], [13] ]
    to generate_and_save_chart function.
    """

    def generate_and_save_chart(
        self, title, REST_VALUES, GRAPHQL_VALUES, is_before_opt=True
    ):
        path_to_save = env("DIR_BEFORE_OPT")
        if not is_before_opt:
            path_to_save = env("DIR_AFTER_OPT")
        main_plot = plt.figure()
        disp_plot = main_plot.add_subplot(111)
        disp_plot.scatter(REST_VALUES[0], REST_VALUES[1], marker="o", color="red")
        disp_plot.scatter(
            GRAPHQL_VALUES[0], GRAPHQL_VALUES[1], marker="o", color="orange"
        )
        disp_plot.axis(
            [-1, 2, 0, int(max(REST_VALUES[1][0], GRAPHQL_VALUES[1][0])) + 2]
        )
        disp_plot.set_title(f"{title}")
        disp_plot.set_xlabel("Architectures")
        disp_plot.set_ylabel("Execution Times[s]")

        for values_set in [REST_VALUES, GRAPHQL_VALUES]:
            plt.text(values_set[0][0], values_set[1][0], values_set[1][0])

        plt.savefig(f'{path_to_save}/{title.replace(" ", "")}.png', dpi=300)
        plt.clf()

    def start(self, is_before_opt):
        compare_result_data = open(env("FILE_FOR_RESEARCHES_DATA"), "r+")
        compare_result_data = json.loads(compare_result_data.readlines()[0])
        for title, val in compare_result_data.items():
            keys_list = list(val.keys())
            values_list = list(val.values())
            REST_VALUES = [[keys_list[0]], [float(values_list[0])]]
            GRAPHQL_VALUES = [[keys_list[1]], [float(values_list[1])]]
            self.generate_and_save_chart(
                title, REST_VALUES, GRAPHQL_VALUES, is_before_opt
            )
