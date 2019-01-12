__author__ = 'pentaa'
from framework.cell import Cell
from framework.geoutililty import *
import simplekml
import numpy as np
class Grid:

    def __init__(self):
        self.mapping_uni_bi_index = None
        self.list_centers_cell_lng_lat = None
        self.list_coords_cell_lng_lat = None
        self.list_cell = []
        self.radius_cell = None
        self.lat_center = None
        self.lng_center = None
        self.radius_container = None
        self.container_cell = None
        self.precision = None
        self.with_precision = None
        self.polygon_4326 = None

        return None

    def init_grid_model(self,bouding_box_lng_lat_radius_meter, selected_radius_cell, with_precision=False, precision=4):
        assert (precision > 0)
        assert len(
            bouding_box_lng_lat_radius_meter) > 2, 'bouding box should be a tuple :(lng_center, lat_center, radius)'

        self.lat_center = bouding_box_lng_lat_radius_meter[1]
        self.lng_center = bouding_box_lng_lat_radius_meter[0]

        self.radius_container = bouding_box_lng_lat_radius_meter[2]

        self.container_cell = Cell(self.radius_container, uni_index=-1, bi_index=[0, 0], with_precision=with_precision,
                                   precision=precision)

        self.container_cell.set_center_as_lng_lat_in_4326(self.lng_center, self.lat_center)
        self.container_cell.create_cell()

        self.precision = precision
        self.with_precision = with_precision


        self.radius_cell = selected_radius_cell

        self.polygon_4326 = self.container_cell.polygon_4326

        assert self.radius_cell < self.radius_container, 'Radius of the cell too big'

    def create_grid(self,bouding_box_lng_lat_radius_meter, selected_radius_cell, with_precision=False, precision=4):

        self.init_grid_model(bouding_box_lng_lat_radius_meter, selected_radius_cell, with_precision, precision)

        index = 0
        index_d1 = 0
        for item_lat_3857 in range(int(self.container_cell.sw_3857.GetY()),
                                   int(self.container_cell.nw_3857.GetY()) + self.radius_cell,
                                   2 * self.radius_cell):
            index_d2 = 0

            for item_lng_3857 in range(int(self.container_cell.sw_3857.GetX()),
                                       int(self.container_cell.se_3857.GetX()) + self.radius_cell,
                                       2 * self.radius_cell):
                item_lng_4326, item_lat_4326 = conversion_point_lng_lat_3857_2_4326(item_lng_3857, item_lat_3857)

                cell_4326 = Cell(self.radius_cell, uni_index=index, bi_index=[index_d1, index_d2],
                                 with_precision=self.with_precision, precision=self.precision)

                cell_4326.set_center_as_lng_lat_in_4326(item_lng_4326, item_lat_4326)
                cell_4326.create_cell()

                self.list_cell.append(cell_4326)

                index_d2 += 1

                index += 1

            index_d1 += 1


    def get_list_cell_lng_lat_center_index(self):
        if self.list_centers_cell_lng_lat is None:
            self.list_centers_cell_lng_lat = [
                [(item.center_4326.GetX(), item.center_4326.GetY()), item.uni_index, item.bi_index] for item in
                self.list_cell]
            return self.list_centers_cell_lng_lat
        else:
            return self.list_centers_cell_lng_lat


    def get_list_cell_lng_lat_coord_as_bb_clock_wise(self):
        if self.list_coords_cell_lng_lat is None:
            self.list_coords_cell_lng_lat = [
                [item.get_lng_lat_list_clock_wise_4326_with_center()[0], item.uni_index, item.bi_index] for item in
                self.list_cell]
            return self.list_coords_cell_lng_lat
        else:
            return self.list_coords_cell_lng_lat


    def is_point_lng_lat_contained_in_grid(self, lng, lat):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AssignSpatialReference(self.spatialReference_4326)
        point.AddPoint(lng, lat)
        return self.polygon_4326.Contains(point)


    def load_grid_from_file(self,filename, with_precision=False, precision=4):

        l = [item.strip().split('@') for item in open(filename, 'r').readlines()]
        center_grid = l[0]
        in_lat_center = float(center_grid[1])
        in_lng_center = float(center_grid[0])
        in_radius_container = int(center_grid[2])
        in_radius_cell= int(center_grid[3])

        self.init_grid_model([in_lat_center, in_lng_center, in_radius_container], in_radius_cell, with_precision, precision)

        for item in l[1:]:
            cell = Cell(self.radius_cell, uni_index=int(item[2]), bi_index=[int(item[3]), int(item[4])])
            cell.set_center_as_lng_lat_in_4326(float(item[0]), float(item[1]))
            cell.create_cell()
            self.list_cell.append(cell)

    def save_grid_as_txtfile(self,filename):

        with open(filename,'w') as fgrid:
            fgrid.write('%.10f@%.10f@%d@%d\n' % (self.lng_center, self.lat_center, self.radius_container, self.radius_cell))
            fgrid.write('\n'.join(['%.10f@%.10f@%d@%d@%d' % (cell.center_4326.GetX(),
                                                             cell.center_4326.GetY(), cell.uni_index,
                                                             cell.bi_index[0],
                                                             cell.bi_index[1])
                                   for cell in self.list_cell]))



    def save_grid_as_kmlfile(self,filename, name='grid',description='spatial grid created with http://bit.ly/2H3hABY'):
        assert len(self.list_cell)>0, 'The list of cells should be greater than 0'

        import random


        kml = simplekml.Kml()
        kml.name = name
        kml.description = description

        for index_cell,cell in enumerate(self.list_cell):
            coords = []
            points,center = cell.get_lng_lat_list_clock_wise_4326_with_center()
            for point in points:
                coords.append(point)
            coords.append(points[0])

            poly = kml.newpolygon(name=str(index_cell),
                               outerboundaryis=coords,innerboundaryis=coords)

            pnt = kml.newpoint(name=str(index_cell),
                               coords=center)

            #rgbl = ['501400FF', '5014B446', '50F0AA14']
            #random.shuffle(rgbl)
            #poly.style.polystyle.color = rgbl[0]
            #if you would like to add style
            #pnt.style.labelstyle.scale = 0.3  # Text 1/2 as big
            ##pnt.style.iconstyle.color = s  # Blue
            #pnt.style.iconstyle.scale = 0.8  # Icon 1 as big
            #l1='http://maps.google.com/mapfiles/kml/shapes/man.png'
            #l2 = 'http://maps.google.com/mapfiles/kml/shapes/woman.png'
            #l3= 'http://maps.google.com/mapfiles/kml/shapes/bars.png'
            #l = [l1,l2,l3]
            #random.shuffle(l)
            #pnt.style.iconstyle.icon.href = l[0]

        kml.save(filename)

    def get_mapping_cell_index_lng_lat(self):
        _dict = {}
        for item in self.list_cell:
            _dict[item.uni_index] = [item.center_4326.GetX(),item.center_4326.GetY()]

        return _dict

    def save_mapping_cell_index_lng_lat(self, filename):
        with open(filename, 'w') as f:
            _dict = self.get_mapping_cell_index_lng_lat()
            l = ['%d:%.10f@%.10f' % (item,_dict[item][0], _dict[item][1])for item in _dict]
            f.write('\n'.join(l))

    @staticmethod
    def load_mapping_cell_index_lng_lat(filename):
        _dict = {}
        with open(filename, 'r') as f:
            for item in f:
                key, values = item.split(':')
                lng, lat = list(map(float, values.split('@')))
                _dict[int(key)] = [lng, lat]
        return  _dict

    def get_mapping_uni_bi_index(self):

        if self.mapping_uni_bi_index is None:
            self.mapping_uni_bi_index = {}
            for item in self.list_cell:
                self.mapping_uni_bi_index[item.uni_index] = item.bi_index
            return self.mapping_uni_bi_index
        else:
            return self.mapping_uni_bi_index

    def get_row_col_dim(self):
        d = self.get_mapping_uni_bi_index()
        x = []
        y = []
        for key in d:
            x.append(d[key][0])
            y.append(d[key][1])

        return max(x)+1, max(y)+1

    def save_mapping_uni_bi_index(self, filename):
        d = self.get_mapping_uni_bi_index()
        with open(filename,'w') as f:
            l = ['%d:%d;%d' % (item, d[item][0], d[item][1]) for item in d]
            f.write('\n'.join(l))

    @staticmethod
    def load_mapping_uni_bi_index(filename):
        dict_uni_bi_index = {}
        with open(filename,'r') as fin:
            for item in fin.readlines():
                uni_index_cell, values = item.strip().split(':')
                bi_indedx_cell_x, bi_indedx_cell_y = values.split(';')
                dict_uni_bi_index[int(uni_index_cell)] = [int(bi_indedx_cell_x), int(bi_indedx_cell_y)]
        return dict_uni_bi_index



if __name__ == "__main__":
    lng_center = -0.06069
    lat_center = 51.5437
    radius_center = 1000
    radius_cell = 100

    grid = Grid()
    grid.create_grid([lng_center, lat_center, radius_center], radius_cell)
    grid.save_grid_as_txtfile('../data/prova.txt')
    grid.save_grid_as_kmlfile('../data/prova.kml')
    print(grid.list_cell)
    grid_saved = Grid()
    grid_saved.load_grid_from_file('../data/prova.txt')
    print(grid_saved.list_cell)

