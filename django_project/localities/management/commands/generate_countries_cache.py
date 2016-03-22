# -*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from localities.models import Country, Locality
import os
import json
from django.conf import settings
from localities.api import get_statistic
from django.core.serializers.json import DjangoJSONEncoder


class Command(BaseCommand):
    help = 'Import Localities from CSV file'

    def handle(self, *args, **options):

        countries = Country.objects.all()

        try:
            # write world cache
            filename = os.path.join(
                    settings.CLUSTER_CACHE_DIR,
                    'world_statistic')
            healthsites = Locality.objects.all()
            output = get_statistic(healthsites)
            print output
            result = json.dumps(output, cls=DjangoJSONEncoder)
            file = open(filename, 'w')
            file.write(result)  # python will convert \n to os.linesep
            file.close()  # you can omit in most cases as the destructor will call it
            print "world cache is finished"
        except Exception as ex:
            print "skip world"

        for country in countries:
            try:
                polygons = country.polygon_geometry

                # write country cache
                filename = os.path.join(
                        settings.CLUSTER_CACHE_DIR,
                        country.name + '_statistic'
                )
                healthsites = Locality.objects.in_polygon(
                        polygons)
                output = get_statistic(healthsites)
                result = json.dumps(output, cls=DjangoJSONEncoder)
                file = open(filename, 'w')
                file.write(result)  # python will convert \n to os.linesep
                file.close()  # you can omit in most cases as the destructor will call it
                print country.name + " cache is finished"
            except:
                print "skip"