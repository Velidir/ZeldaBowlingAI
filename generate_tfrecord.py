import tensorflow as tf
import xmltodict
import os
import io
from object_detection.utils import dataset_util


flags = tf.app.flags
flags.DEFINE_string('output_path', 'TFRecords', 'Path to output TFRecord')
flags.DEFINE_string('input_path', 'BoTWpics/train/', 'Path to input xml')
FLAGS = flags.FLAGS


def create_tf_example(xmlfile):
  # TODO(user): Populate the following variables from your example.
  path = FLAGS.input_path+xmlfile
  with open(path) as fd:
      doc = xmltodict.parse(fd.read())

  height = doc['annotation']['size']['height'] # Image height
  width = doc['annotation']['size']['width'] # Image width
  filename = doc['annotation']['path'] # Filename of the image. Empty if image is not from file
  with tf.gfile.GFile(filename, 'rb') as fid:
    encoded_jpg = fid.read()
  encoded_image_data = io.BytesIO(encoded_jpg) # Encoded image bytes
  image_format = b'png' # b'jpeg' or b'png'
  xmins = []  # List of normalized left x coordinates in bounding box (1 per box)
  xmaxs = []  # List of normalized right x coordinates in bounding box
  # (1 per box)
  ymins = []  # List of normalized top y coordinates in bounding box (1 per box)
  ymaxs = []  # List of normalized bottom y coordinates in bounding box
  # (1 per box)
  classes_text = []  # List of string class name of bounding box (1 per box)
  classes = []  # List of integer class id of bounding box (1 per box)

  for obj in doc['annotation']['object']:
      xmins.append(obj['bndbox']['xmin'])
      xmaxs.append(obj['bndbox']['xmax'])
      ymins.append(obj['bndbox']['ymin'])
      ymaxs.append(obj['bndbox']['ymax'])
      classes_text.append(obj['name'])
      if obj['name'] is 'link':
        classes.append(1)
      elif obj['name'] is 'dude':
        classes.append(2)
      elif obj['name'] is 'totem':
        classes.append(3)
      else:
        classes.append(4)

  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(filename),
      'image/source_id': dataset_util.bytes_feature(filename),
      'image/encoded': dataset_util.bytes_feature(encoded_image_data),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
  }))
  return tf_example


def main(_):
  writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

  # Loop through all xml files
  for file in os.listdir(FLAGS.input_path):
      if not file.endswith('.xml'):
          continue
      else:
          tf_example = create_tf_example(file)
          writer.write(tf_example.SerializeToString())
  writer.close()


if __name__ == '__main__':
  tf.app.run()