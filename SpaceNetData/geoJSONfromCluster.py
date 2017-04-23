
from osgeo import gdal, ogr
import os

def CreateGeoJSON (folder, fn, cluster, geom, proj ):
    """

    :param fn: IMAGE id
    :param cluster: matrix or detected result (one band)
    :param geom: the image (detected) geo information
    :param proj: the image (detected) project information
    :return:
    """
    memdrv = gdal.GetDriverByName ('MEM')
    src_ds = memdrv.Create('',cluster.shape[1],cluster.shape[0],1)
    src_ds.SetGeoTransform(geom)
    src_ds.SetProjection(proj)
    band = src_ds.GetRasterBand(1)
    band.WriteArray(cluster)
    dst_layername = "BuildingID"
    drv = ogr.GetDriverByName("geojson")

    file_name = fn +'_'+ dst_layername + ".geojson"
    save_path = os.path.join(folder,file_name)

    if os.path.exists(save_path):
        drv.DeleteDataSource(save_path)
        # return save_path  #  for test other part of codes

    dst_ds = drv.CreateDataSource ( save_path)
    dst_layer = dst_ds.CreateLayer( dst_layername, srs=None )
    dst_layer.CreateField( ogr.FieldDefn("DN", ogr.OFTInteger) )
    gdal.Polygonize( band  , None, dst_layer, 0, ['8CONNECTED=8'], callback=None )
    return save_path