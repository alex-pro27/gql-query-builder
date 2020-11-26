# coding: utf-8


class GqlQuery():
    def __init__(self):
        self.object = ''
        self.return_field =  ''
        self.query_field = ''
        self.operation_field = ''
        self.fragment_field = ''

    def remove_duplicate_spaces(self, query):
        return " ".join(query.split())

    def fields(self, fields, name = '', condition_expression = ''):
        query = '{ ' + " ".join(fields) + ' }'
        if name:
            if condition_expression:
                query = '{name} {condition_expression} {query}'.format(name=name, condition_expression=condition_expression, query=query)
            else:
                query = '{name} {query}'.format(name=name, query=query)
        self.return_field = query
        return self

    def query(self, name, alias = '', input=None):
        self.query_field = name
        inputs  = []
        if input:
            for key, value in input.items():
                inputs.append('{key}: {value}'.format(key=key, value=value))
            self.query_field = self.query_field + '(' + ", ".join(inputs) + ')'
        if alias:
            self.query_field = '{alias}: {query_field}'.format(alias=alias, query_field=self.query_field)

        return self

    def operation(self, query_type='query', name='', input=None, queries=None):
        self.operation_field = query_type
        inputs = []
        if name:
            self.operation_field = '{operation_field} {name}'.format(operation_field=self.operation_field, name=name)
            if input:
                for key, value in input.items():
                    inputs.append('{key}: {value}'.format(key=key, value=value))
                self.operation_field = self.operation_field + '(' + ", ".join(inputs) + ')'

        if queries:
            self.object = self.operation_field + ' { ' + " ".join(queries) + ' }'

        return self

    def fragment(self, name, interface):
        self.fragment_field = 'fragment {name} on {interface}'.format(name=name, interface=interface)
        return self

    def generate(self):
        if self.fragment_field:
            self.object = '{fragment_field} {return_field}'.format(fragment_field=self.fragment_field, return_field=self.return_field)
        else:
            if self.object == '' and self.operation_field == '' and self.query_field == '':
                self.object = self.return_field
            elif self.object == '' and self.operation_field == '':
                self.object = self.query_field + ' ' + self.return_field
            elif self.object == '':
                self.object = self.operation_field + ' { ' + self.query_field + ' ' + self.return_field + ' }'

        return self.remove_duplicate_spaces(self.object)
