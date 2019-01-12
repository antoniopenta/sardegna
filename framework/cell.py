from osgeo import ogr, osr

class Cell:

    def __init__(self,radius,uni_index=0, bi_index=[],with_precision=False,precision=4):
        assert(precision>0)
        self.spatialReference_3857 = osr.SpatialReference()
        self.spatialReference_3857.ImportFromEPSG(3857)
        self.spatialReference_4326 = osr.SpatialReference()
        self.spatialReference_4326.ImportFromEPSGA(4326)
        self.coordTrans_4326_2_3857 = osr.CoordinateTransformation(self.spatialReference_4326,self.spatialReference_3857)
        self.coordTrans_3857_2_4326 = osr.CoordinateTransformation(self.spatialReference_3857,self.spatialReference_4326)
        self.uni_index = uni_index
        self.bi_index =  bi_index
        self.center_3857 = None
        self.center_4326 = None
        self.radius = None
        self.nw_3857 = None
        self.ne_3857 = None
        self.sw_3857 = None
        self.se_3857 = None
        self.nw_4326 = None
        self.ne_4326 = None
        self.sw_4326 = None
        self.se_4326 = None
        self.polygon_4326 = None
        self.precision = precision
        self.with_precision = with_precision
        self.radius = radius


    def set_center_as_lng_lat_in_3857(self, lng, lat):

        self.center_3857 = ogr.Geometry(ogr.wkbPoint)
        self.center_3857.AssignSpatialReference(self.spatialReference_3857)
        self.center_3857.AddPoint(lng, lat)
        self.center_4326 = self.center_3857.Clone()
        self.center_4326.Transform(self.coordTrans_3857_2_4326)
        return self

    def set_center_as_lng_lat_in_4326(self, lng, lat):

        self.center_4326 = ogr.Geometry(ogr.wkbPoint)
        self.center_4326.AssignSpatialReference(self.spatialReference_4326)
        self.center_4326.AddPoint(lng,lat)

        self.center_3857 = self.center_4326.Clone()
        self.center_3857.Transform(self.coordTrans_4326_2_3857)
        return self


    def create_cell(self):

        assert(self.center_3857 is not None or self.center_4326 is not None),'we cannot create a cell withour setting first the center'
        self.nw_3857 = ogr.Geometry(ogr.wkbPoint)
        self.nw_3857.AssignSpatialReference(self.spatialReference_3857)
        self.nw_3857.AddPoint(self.center_3857.GetX()-self.radius,self.center_3857.GetY()+self.radius)
        self.nw_4326 = self.nw_3857.Clone()
        self.nw_4326.Transform(self.coordTrans_3857_2_4326)
        self.ne_3857 = ogr.Geometry(ogr.wkbPoint)
        self.ne_3857.AssignSpatialReference(self.spatialReference_3857)
        self.ne_3857.AddPoint(self.center_3857.GetX()+self.radius,self.center_3857.GetY()+self.radius)
        self.ne_4326 = self.ne_3857.Clone()
        self.ne_4326.Transform(self.coordTrans_3857_2_4326)
        self.se_3857 = ogr.Geometry(ogr.wkbPoint)
        self.se_3857.AssignSpatialReference(self.spatialReference_3857)
        self.se_3857.AddPoint(self.center_3857.GetX()+self.radius,self.center_3857.GetY()-self.radius)
        self.se_4326 = self.se_3857.Clone()
        self.se_4326.Transform(self.coordTrans_3857_2_4326)
        self.sw_3857 = ogr.Geometry(ogr.wkbPoint)
        self.sw_3857.AssignSpatialReference(self.spatialReference_3857)
        self.sw_3857.AddPoint(self.center_3857.GetX()-self.radius,self.center_3857.GetY()-self.radius)
        self.sw_4326 = self.sw_3857.Clone()
        self.sw_4326.Transform(self.coordTrans_3857_2_4326)
        ring_4326 = ogr.Geometry(ogr.wkbLinearRing)
        ring_4326.AddPoint(self.nw_4326.GetX(),self.nw_4326.GetY())
        ring_4326.AddPoint(self.ne_4326.GetX(),self.ne_4326.GetY())
        ring_4326.AddPoint(self.se_4326.GetX(),self.se_4326.GetY())
        ring_4326.AddPoint(self.sw_4326.GetX(),self.sw_4326.GetY())
        ring_4326.CloseRings()
        self.polygon_4326 = ogr.Geometry(ogr.wkbPolygon)
        self.polygon_4326.AddGeometry(ring_4326)
        return self

    def is_point_lng_lat_contained_in_cell(self, lng, lat):

        point = ogr.Geometry(ogr.wkbPoint)
        point.AssignSpatialReference(self.spatialReference_4326)
        point.AddPoint(lng, lat)
        return self.polygon_4326.Contains(point)




    def get_lng_lat_list_clock_wise_4326_with_center(self):

        if self.with_precision:
            nw = (round(self.nw_4326.GetX(),self.precision), round(self.nw_4326.GetY(),self.precision))
            ne = (round(self.ne_4326.GetX(),self.precision), round(self.ne_4326.GetY(),self.precision))
            sw = (round(self.sw_4326.GetX(),self.precision), round(self.sw_4326.GetY(),self.precision))
            se = (round(self.se_4326.GetX(),self.precision), round(self.se_4326.GetY(),self.precision))
            return [ne, se, sw, nw], [(round(self.center_4326.GetX(),self.precision),round(self.center_4326.GetY(),self.precision))]
        else:
            nw = (self.nw_4326.GetX(), self.nw_4326.GetY())
            ne = (self.ne_4326.GetX(), self.ne_4326.GetY())
            sw = (self.sw_4326.GetX(), self.sw_4326.GetY())
            se = (self.se_4326.GetX(), self.se_4326.GetY())
            return [ne, se, sw, nw], [(self.center_4326.GetX(),self.center_4326.GetY())]

    def get_lat_lng_list_clock_wise_4326_with_center(self):

        if self.with_precision:
            nw = (round(self.nw_4326.GetY(),self.precision), round(self.nw_4326.GetX(),self.precision))
            ne = (round(self.ne_4326.GetY(),self.precision), round(self.ne_4326.GetX(),self.precision))
            sw = (round(self.sw_4326.GetY(),self.precision), round(self.sw_4326.GetX(),self.precision))
            se = (round(self.se_4326.GetY(),self.precision), round(self.se_4326.GetX(),self.precision))
            return [ne, se, sw, nw], [(round(self.center_4326.GetY(),self.precision),round(self.center_4326.GetX(),self.precision))]
        else:
            nw = (self.nw_4326.GetY(), self.nw_4326.GetX())
            ne = (self.ne_4326.GetY(), self.ne_4326.GetX())
            sw = (self.sw_4326.GetY(), self.sw_4326.GetX())
            se = (self.se_4326.GetY(), self.se_4326.GetX())
            return [ne, se, sw, nw], [(self.center_4326.GetY(),self.center_4326.GetX())]

    def __str__(self):
        return  '%0.5f %0.5f %d'%(self.center_4326.getX(),self.center_4326.getY(),self.radius)


    def __repr__(self):
        return '%0.5f %0.5f %d' % (self.center_4326.GetX(), self.center_4326.GetY(), self.radius)
