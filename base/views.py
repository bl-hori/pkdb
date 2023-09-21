import pandas as pd
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


def home(request):
    template = loader.get_template("base/home.html")
    ctx = {"title": "Django Home"}
    return HttpResponse(template.render(ctx, request))


class GetPokemonList(TemplateView):
    template_name = "base/list.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        parameters = self.request.GET

        #
        url = "https://graphqlpokemon.favware.tech/v7"
        transport = RequestsHTTPTransport(url=url)

        #
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""
            {
                getAllPokemon {
                    key
                    sprite
                    num
                    types {
                        name
                    }
                    flavorTexts {
                        flavor
                    }
                }
            }
        """)
        result = client.execute(query)

        data = result["getAllPokemon"]
        df = pd.DataFrame(data)

        df = df[df["num"] > 0].sample(51)
        df['types'] = df['types'].map(lambda l: ', '.join([v['name'] for v in l]))
        df['flavorTexts'] = df['flavorTexts'].map(lambda x: x[0]['flavor'])

        pokemon_list = df.to_dict(orient="records")

        ctx['pokemon_list'] = pokemon_list

        return ctx


class GetPokemonDetail(TemplateView):
    template_name = "base/detail.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        parameters = self.request.GET

        key = ctx.get('key', None)
        if key:
            #
            url = "https://graphqlpokemon.favware.tech/v7"
            transport = RequestsHTTPTransport(url=url)

            #
            client = Client(transport=transport, fetch_schema_from_transport=True)

            query = gql('''
                {
                    getPokemon(pokemon: {key}) {
                        key
                        sprite
                        num
                        types {
                            name
                        }
                        flavorTexts {
                            flavor
                        }
                        evolutions {
                            key
                            sprite
                            num
                            types {
                                name
                            }
                            flavorTexts {
                                flavor
                            }
                        }
                    }
                }
            '''.replace('{key}', key))

            result = client.execute(query)
            data = [result["getPokemon"]]
            df = pd.DataFrame(data)

            df['types'] = df['types'].map(lambda l: ', '.join([v['name'] for v in l]))
            df['flavorTexts'] = df['flavorTexts'].map(lambda x: x[0]['flavor'])

            pokemon = df.to_dict(orient='records')[0]
            print(pokemon)
            ctx['pokemon'] = pokemon

            if data[0]['evolutions']:
                df_ev = pd.DataFrame(df['evolutions'].to_dict()[0])
                df_ev['types'] = df_ev['types'].map(lambda l: ', '.join([v['name'] for v in l]))
                df_ev['flavorTexts'] = df_ev['flavorTexts'].map(lambda x: x[0]['flavor'])
                evolution_list = df_ev.to_dict('records')
                print(evolution_list)

                ctx['evolution_list'] = evolution_list

        return ctx