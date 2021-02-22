# P2Y(Pascal to Yolo)
Pascal VOC annotation to YOLO label converter

## Usage
pascal_voc_annotation_path : annotation xml files path<br>

## Convert
Input format : Pascal VOC annotation xml
```xml
<annotation>
    <folder>images</folder>
    <filename>maksssksksss0.png</filename>
    <size>
        <width>512</width>
        <height>366</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>without_mask</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <occluded>0</occluded>
        <difficult>0</difficult>
        <bndbox>
            <xmin>79</xmin>
            <ymin>105</ymin>
            <xmax>109</xmax>
            <ymax>142</ymax>
        </bndbox>
    </object>
    <object>
        <name>with_mask</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <occluded>0</occluded>
        <difficult>0</difficult>
        <bndbox>
            <xmin>185</xmin>
            <ymin>100</ymin>
            <xmax>226</xmax>
            <ymax>144</ymax>
        </bndbox>
    </object>
    <object>
        <name>without_mask</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <occluded>0</occluded>
        <difficult>0</difficult>
        <bndbox>
            <xmin>325</xmin>
            <ymin>90</ymin>
            <xmax>360</xmax>
            <ymax>141</ymax>
        </bndbox>
    </object>
</annotation>
```

Output format : YOLO label
```
0 0.183593 0.337431 0.058593 0.101092
1 0.401367 0.333333 0.080078 0.120218
0 0.668945 0.315573 0.068359 0.139344
```

## classes.txt
If there were classes.txt with the xml files, the original index order is maintained while converting.

Otherwise, the order of the class indexes can be newly defined.

Example of newly defined classes.txt
```
without_mask
with_mask
mask_weared_incorrect
```
