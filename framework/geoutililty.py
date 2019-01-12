from math import sin, cos, sqrt, atan2, radians,pi
from osgeo import ogr, osr, gdal
from simplekml import Kml,Color,AltitudeMode,Style



def conversion_point_lng_lat_3857_2_4326(lng, lat):

    spatialReference_3857 = osr.SpatialReference()
    spatialReference_3857.ImportFromEPSG(3857)
    spatialReference_4326 = osr.SpatialReference()
    spatialReference_4326.ImportFromEPSGA(4326)
    coordTrans_4326_2_3857 = osr.CoordinateTransformation(spatialReference_4326,spatialReference_3857)
    coordTrans_3857_2_4326 = osr.CoordinateTransformation(spatialReference_3857,spatialReference_4326)

    point = ogr.Geometry(ogr.wkbPoint)
    point.AssignSpatialReference(spatialReference_3857)
    point.AddPoint(lng, lat)
    point.Transform(coordTrans_3857_2_4326)

    return point.GetX(), point.GetY()


def conversion_point_lng_lat_4326_2_3857(lng, lat):

    spatialReference_3857 = osr.SpatialReference()
    spatialReference_3857.ImportFromEPSG(3857)
    spatialReference_4326 = osr.SpatialReference()
    spatialReference_4326.ImportFromEPSGA(4326)
    coordTrans_4326_2_3857 = osr.CoordinateTransformation(spatialReference_4326,spatialReference_3857)
    coordTrans_3857_2_4326 = osr.CoordinateTransformation(spatialReference_3857,spatialReference_4326)

    point = ogr.Geometry(ogr.wkbPoint)
    point.AssignSpatialReference(spatialReference_4326)
    point.AddPoint(lng, lat)
    point.Transform(coordTrans_4326_2_3857)

    return point.GetX(), point.GetY()








def haversine_distance_lon_lat(p1_lon_lat, p2_lon_lat):
    # approximate radius of earth in km
    R = 6373.0

    lon1 = radians(p1_lon_lat[0])
    lat1 = radians(p1_lon_lat[1])
    lon2 = radians(p2_lon_lat[0])
    lat2 = radians(p2_lon_lat[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance_km = R * c
    distance_m = distance_km*1000
    #return in km
    return  distance_km, distance_m


def increment_lon_lat_by_delta(lon,lat,offset_lon_meter, offset_lat_meter):

    spatialReference_3857 = osr.SpatialReference()
    spatialReference_3857.ImportFromEPSG(3857)
    spatialReference_4326 = osr.SpatialReference()
    spatialReference_4326.ImportFromEPSGA(4326)
    coordTrans_4326_2_3857 = osr.CoordinateTransformation(spatialReference_4326,spatialReference_3857)
    coordTrans_3857_2_4326 = osr.CoordinateTransformation(spatialReference_3857,spatialReference_4326)
    point_4326 = ogr.Geometry(ogr.wkbPoint)
    point_4326.AssignSpatialReference(spatialReference_4326)
    point_4326.AddPoint(lon, lat)
    point_3857 = point_4326.Clone()
    point_3857.Transform(coordTrans_4326_2_3857)
    new_point_3857 = ogr.Geometry(ogr.wkbPoint)
    new_point_3857.AssignSpatialReference(spatialReference_3857)
    new_point_3857.AddPoint(point_3857.GetX()+offset_lon_meter,point_3857.GetY()+offset_lat_meter)
    new_point_3857.Transform(coordTrans_3857_2_4326)
    return new_point_3857.GetX(),new_point_3857.GetY()







def serialize_list_point_lon_lat_index_as_kml(list_points, name='point', color=Color.green, scale=1, abolutefilepath ='points.kml'):

    kml = Kml()
    point_folder = kml.newfolder(name='points')
    for point in list_points:
        lon_lat = [point[0],point[1]]
        index = point[2]
        pnt_0 = point_folder.newpoint()
        pnt_0.name = str(index)
        pnt_0.coords = [lon_lat]
        pnt_0.labelstyle.color=color
        pnt_0.style.labelstyle.scale = scale
        pnt_0.style.iconstyle.icon.href='http://maps.google.com/mapfiles/kml/paddle/grn-circle-lv.png'
    kml.save(abolutefilepath)



def serialize_list_point_lon_lat_index_as_line_in_kml(list_points, name='point', color=Color.green, scale=1, abolutefilepath ='line.kml'):

    kml = Kml()

    point_folderlin = kml.newlinestring(name="line", description="line",
                        coords=list_points)
    point_folderlin.labelstyle.color=color
    point_folderlin.style.labelstyle.scale = scale
    point_folderlin.style.iconstyle.icon.href='http://maps.google.com/mapfiles/kml/paddle/grn-circle-lv.png'

    point_folder = kml.newfolder(name='points')
    for point in list_points:
        lon_lat = [point[0],point[1]]
        index = point[2]
        pnt_0 = point_folder.newpoint()
        pnt_0.name = str(index)
        pnt_0.coords = [lon_lat]
        pnt_0.labelstyle.color=color
        pnt_0.style.labelstyle.scale = scale
        pnt_0.style.iconstyle.icon.href='http://maps.google.com/mapfiles/kml/paddle/grn-circle-lv.png'


    kml.save(abolutefilepath)


def save_geometry_in_postgis(geometry,table,type_ogr,database='lasie',usr='postgres',pw='antonio'):


    connectionString = "PG:dbname='%s' user='%s' password='%s'" % (database,usr,pw)
    ogrds = ogr.Open(connectionString)

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)

    layer = ogrds.CreateLayer(table, srs,type_ogr, ['OVERWRITE=YES'] )

    layerDefn = layer.GetLayerDefn()

    feature = ogr.Feature(layerDefn)
    feature.SetGeometry(geometry)

    layer.StartTransaction()
    layer.CreateFeature(feature)
    layer.CommitTransaction()




#if __name__=='__main__':

    # lon = 116.4080
    # lat = 39.9127
    # lon_meter, lat_meter = conversion_point_lon_lat_4326_2_3857((lon, lat))
    # print(lon_meter, lat_meter
    # lon_2, lat_2 = conversion_point_lon_lat_3857_2_4326((lon_meter, lat_meter))
    # print lon_2, lat_2
    #
    # lon_1, lat_1 = increment_lon_lat_by_delta(lon, lat, 500, 500)
    # lon_2, lat_2 = increment_lon_lat_by_delta(lon, lat, 500, -500)
    # lon_3, lat_3 = increment_lon_lat_by_delta(lon, lat, -500, -500)
    # lon_4, lat_4 = increment_lon_lat_by_delta(lon, lat, -500, +500)
    #
    # l = []
    #
    # l.append((lon_1, lat_1))
    # l.append((lon_2, lat_2))
    # l.append((lon_3, lat_3))
    # l.append((lon_4, lat_4))
    #
    # serialize_list_point_lon_lat_index_as_kml(l)
    #
    # print haversine_distance_lon_lat((lon,lat),(lon_1,lat_1))*1000
