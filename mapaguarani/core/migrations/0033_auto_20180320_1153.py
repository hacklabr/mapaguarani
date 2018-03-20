# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20180319_1128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actionfield',
            options={'verbose_name_plural': 'Action Fields', 'verbose_name': 'Action Field'},
        ),
        migrations.AlterModelOptions(
            name='archaeologicalimage',
            options={'verbose_name_plural': 'Archaeological Images', 'verbose_name': 'Archaeological Image'},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'verbose_name_plural': 'Organizations', 'verbose_name': 'Organization'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name_plural': 'Projects', 'verbose_name': 'Project'},
        ),
        migrations.AlterModelOptions(
            name='projectfile',
            options={'verbose_name_plural': 'Project Files', 'verbose_name': 'Project File'},
        ),
        migrations.AlterModelOptions(
            name='projectlink',
            options={'verbose_name_plural': 'Project Links', 'verbose_name': 'Project Link'},
        ),
        migrations.AlterField(
            model_name='archaeologicalplace',
            name='geometry',
            field=django.contrib.gis.db.models.fields.PointField(verbose_name='Geometry', srid=4326),
        ),
        migrations.AlterField(
            model_name='document',
            name='name',
            field=models.CharField(max_length=255, help_text='Tipo de Documento, nº  do documento, Órgão Expedidor, Data. Ex: Portaria Declaratória, nº 83, Ministério da Justiça, 12/08/2008', verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='associated_land',
            field=models.ForeignKey(help_text='Caso a terra esteja em processo de revisão, e tanto a terra original quanto a revisada estejam cadastradas,\n                     indique qual outro registro se refere à mesma terra, original ou revisada. ', to='core.IndigenousLand', null=True, blank=True, verbose_name='Associated Land'),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='claim',
            field=models.TextField(help_text=' Campo apenas de visualização restrita, para uso das associações indígenas. Indicar qual a próxima fase do processo de regularização.', verbose_name='Claim', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='demand',
            field=models.TextField(help_text='Campo apenas de visualização restrita, para uso das associações indígenas. Detalhar a demanda atual frente aos órgãos públicos (desintrusão, conclusão de levantamento fundiário ou antropológico, etc..) ', verbose_name='Demand', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='documents',
            field=models.ManyToManyField(to='core.Document', help_text='Acrescente a documentação oficial sobre a terra indígena (decretos de homologação, portarias declaratórias,etc.).\n                     Caso o mesmo documento se refira a mais de uma terra indígena, ele pode já estar cadastrado e você pode apenas selecioná-lo. \n                     Confira na lista antes de adicionar. ', verbose_name='documentation', related_name='indigenousland_documentation', blank=True),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='geometry',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(help_text='Inclua aqui o polígono da terra indígena apenas em formato *.KML. \n                                        Certifique-se de que apenas a terra indígena correspondente está no arquivo. ', verbose_name='Indigenous Land Spatial Data', srid=4326),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='guarani_exclusive_possession_area_portion',
            field=models.FloatField(help_text='Em caso de terras ainda em processo de regularização, caso tenha informação de qual porção da área já foi desintrusada incluir. \n                     Em áreas em que não se iniciou o processo de desintrusão colocar 0.', verbose_name='Guarani full and exclusive portion area possession', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='land_tenure',
            field=models.ForeignKey(help_text='Selecione a fase do processo de regularização em que está a terra. Em caso de terras em processo de revisão de limites, é preciso cadastrar separadamente a Terra Original e a Terra Revisada e detalhar no próximo item.', to='core.LandTenure', verbose_name='Land Tenure', related_name='indigenous_lands'),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='land_tenure_status',
            field=models.ForeignKey(help_text='Selecione “Não Delimitada” para as terras ainda sem estudo aprovado pela Funai, e portanto, sem limites definidos.\n                     Selecione “Sem Revisão” caso não incida sobre a área nenhum processo de revisão de limites.\n                     Selecione “Terra Original em estudo de Revisão” caso incida sobre a área processo de revisão, mas os novos limites ainda não tenham sido aprovados pela Funai.\n                     Selecione “Terra Original” caso incida sobre a área processo de revisão, os limites já tenham sido aprovados pela Funai, e essa terra seja o polígono da terra original.\n                     Selecione “Terra Revisada” caso incida sobre a área processo de revisão, os limites já tenham sido aprovados pela Funai, e essa terra seja o polígono da terra revisada. ', to='core.LandTenureStatus', verbose_name='Land Tenure Status', related_name='indigenous_lands'),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='layer',
            field=models.ForeignKey(help_text='O sistema é dividido em camadas que configuram as permissões de usuários e as diferentes formas de visualização do mapa.\n                                           Atenção à descrição das camadas para associar corretamente a terra indígena à camada correta.\n                                           Adicionar ou Modificar Documento de Terra Indígena', to='core.MapLayer', verbose_name='Layer', related_name='indigenous_lads'),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='official_area',
            field=models.FloatField(help_text='Indique o tamanho da terra indígena de acordo com fonte oficial.', verbose_name='Official area', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='others_exclusive_possession_area_portion',
            field=models.FloatField(help_text='Em caso de terras ainda em processo de regularização, caso tenha informação de qual porção da área já foi desintrusada incluir. \n                     Em áreas em que não se iniciou o processo de desintrusão colocar 0. ', verbose_name="Other peoples' full and exclusive portion area possession", null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='source',
            field=models.CharField(max_length=512, help_text='Indique de qual base de dados, organização ou pessoa provém o polígono utilizado para a terra indígena.', verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='geometry',
            field=django.contrib.gis.db.models.fields.PointField(help_text='Localize o ponto da aldeia. \n                                              Você pode incluir as coordenadas geográficas (em graus decimais) ou \n                                              localizar o ponto olhando o mapa ou a foto aérea do Google.', verbose_name='Geometry', srid=4326),
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='layer',
            field=models.ForeignKey(help_text='O sistema é dividido em camadas que configuram as permissões de usuários e as\n                                           diferentes formas de visualização do mapa. Atenção à descrição das camadas\n                                           para associar corretamente a aldeia à camada correta', to='core.MapLayer', verbose_name='Layer', related_name='villages'),
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='position_precision',
            field=models.CharField(max_length=256, help_text='Indique se a localização geográfica da aldeia é exata (seja se obtida por GPS ou Google Earth) ou se é aproximada (caso não tenha certeza do ponto exato).', verbose_name='Position Precision', default='no_info', choices=[('exact', 'Exact'), ('approximate', 'Approximate'), ('no_info', 'No information')]),
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='position_source',
            field=models.CharField(max_length=512, help_text='Indique quem foi o responsável pela localização da aldeia.', verbose_name='Position Source'),
        ),
    ]
