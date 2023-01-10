from dataclasses import dataclass
from typing import List

@dataclass
class dataset:
    name:str
    url:str
    color:str

@dataclass
class datasets:
    lod: List[dataset]

    def get_num_datasets(self):
        return len(self.lod)
    def get_datasets_urls(self):
        return [dataset.url for dataset in self.lod]
    def get_datasets_colors(self):
        return [dataset.color for dataset in self.lod]

    def remove_all_datasets(self):
        return datasets(lod = [])

    def remove_one_dataset(self, dataset_name:str):
        for dataset in datasets.lod:
            if dataset_name == dataset.name:
                self.lod.remove(dataset)
            break


@dataclass
class contrast:
    name: str
    datasets: datasets

    def get_datasets_urls(self):
        return self.datasets.get_datasets_urls()

    def get_datasets_colors(self):
        return self.datasets.get_datasets_colors()

    def get_len_datasets(self):
        return len(self.datasets.lod)





@dataclass
class contrasts:
    loc: List[contrast]

    def get_names(self):
        return [contrast.name for contrast in self.loc]

    def get_num_contrasts(self):
        return len(self.loc)

    def get_num_datasets(self):
        val = 0
        for contrast in self.loc:
            val += contrast.get_len_datasets()
        return val

    def remove_all_contrasts(self):
        return contrasts(loc = [])

    def remove_one_contrast(self, contrast_name:str):
        for contrast in contrasts.loc:
            if contrast_name == contrast.name:
                self.loc.remove(contrast)
            break
    def add_one_contrast(self, contrast:contrast):
        self.loc.append(contrast)




# contrast1 = contrast(name = 'cont1', datasets=[])
# contrast2 = contrast(name = 'cont2', datasets=[])

# test = contrasts(contrast1)
# print(test.loc)
# test=test.add_contrast(contrast2)

# print(test.loc)

# TESTS

# ds1 = dataset(name='ds1', url = 'url1', color = 'red')
# datasets1 = datasets(lod = [ds1])
# contrast1 = contrast(name = 'cont1', datasets=datasets1)
# contrasts1 = contrasts(loc = [contrast1])

# print(contrasts1.get_names())

