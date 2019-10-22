import os


class RelMon(object):

    def __init__(self, data):
        self.data = self.__remove_empty_categories(data)
        relmon_path = 'relmons/%s/' % (self.get_id())
        if not os.path.isdir(relmon_path):
            os.mkdir(relmon_path)

    def __remove_empty_categories(self, data):
        non_empty_categories = []
        for category in data.get('categories', []):
            reference_length = len(category['reference'])
            target_length = len(category['target'])
            if reference_length > 0 and target_length > 0:
                non_empty_categories.append(category)

        data['categories'] = non_empty_categories
        return data

    def reset(self):
        self.set_status('new')
        self.set_condor_status('<unknown>')
        self.set_condor_id(0)
        for category in self.data['categories']:
            category['status'] = 'initial'
            category['reference'] = [{'name': x.strip() if isinstance(x, str) else x['name'].strip(),
                                      'file_name': '',
                                      'file_url': '',
                                      'file_size': 0,
                                      'status': 'initial'} for x in category['reference']]
            category['target'] = [{'name': x.strip() if isinstance(x, str) else x['name'].strip(),
                                   'file_name': '',
                                   'file_url': '',
                                   'file_size': 0,
                                   'status': 'initial'} for x in category['target']]

        return self.data

    def get_id(self):
        return self.data.get('id')

    def get_name(self):
        return self.data.get('name')

    def get_cpu(self):
        number_of_relvals = 0
        for category in self.data['categories']:
            number_of_relvals += len(category['reference'])
            number_of_relvals += len(category['target'])

        # Comparisons CPU
        #  0- 10     -  1
        # 11- 25     -  2
        # 26- 60     -  4
        # 61-150     -  8
        # 151+       - 16

        cpus = 1
        if number_of_relvals <= 20:
            # Max 10 vs 10
            cpus = 1
        elif number_of_relvals <= 50:
            # Max 25 vs 25
            cpus = 2
        elif number_of_relvals <= 120:
            # Max 60 vs 60
            cpus = 4
        elif number_of_relvals <= 300:
            # Max 150 vs 150
            cpus = 8
        else:
            # > 150 vs 150
            cpus = 16

        return cpus

    def get_memory(self):
        memory = str(self.get_cpu() * 2) + 'G'
        return memory

    def get_disk(self):
        number_of_relvals = 0
        for category in self.data['categories']:
            number_of_relvals += len(category['reference'])
            number_of_relvals += len(category['target'])

        disk = '%sM' % (number_of_relvals * 300)
        return disk

    def get_json(self):
        return self.data

    def get_status(self):
        return self.data['status']

    def get_condor_status(self):
        return self.data.get('condor_status', '')

    def get_condor_id(self):
        return self.data.get('condor_id', 0)

    def set_status(self, status):
        self.data['status'] = status

    def set_condor_status(self, condor_status):
        self.data['condor_status'] = condor_status

    def set_condor_id(self, condor_id):
        self.data['condor_id'] = condor_id

    def __str__(self):
        return '%s (%s)' % (self.get_name(), self.get_id())

    def __repr__(self):
        return '%s (%s)' % (self.get_name(), self.get_id())
