# datasetshowcaseDETECTION
✅ Found 47 classes in master.yaml           
                  
========================================
📊 DATASET ANALYSIS REPORT                   
========================================

Total Images per Split:
  - Train:      68127 images
  - Valid:      8608 images
  - Test:       4086 images

Total Instances per Class (across all splits):
  - ID  0 | Ants                                     | 2496 instances
  - ID  1 | Bees                                     | 1750 instances
  - ID  2 | Beetles                                  | 1202 instances
  - ID  3 | Black Rust                               | 29 instances
  - ID  4 | Brown Rust                               | 37 instances
  - ID  5 | COW                                      | 14810 instances
  - ID  6 | Caterpillars                             | 1972 instances
  - ID  7 | Corn Gray leaf spot                      | 83 instances
  - ID  8 | Corn leaf blight                         | 403 instances
  - ID  9 | Corn rust leaf                           | 137 instances
  - ID 10 | Early Blight                     
        | 3377 instances
  - ID 11 | Earthworms                       
        | 1195 instances
  - ID 12 | Earwigs                          
        | 1359 instances
  - ID 13 | Grasshoppers                     
        | 1228 instances
  - ID 14 | Healthy                          
        | 3643 instances
  - ID 15 | Healthy Wheat                    
        | 852 instances
  - ID 16 | Late Blight                      
        | 4536 instances
  - ID 17 | Leaf Miner                       
        | 3289 instances
  - ID 18 | Leaf Mold                        
        | 4572 instances
  - ID 19 | Mosaic Virus                     
        | 4282 instances
  - ID 20 | Moths                            
        | 1210 instances
  - ID 21 | Potato leaf                      
        | 203 instances
  - ID 22 | Potato leaf early blight         
        | 396 instances
  - ID 23 | Potato leaf late blight          
        | 302 instances
  - ID 24 | Septoria                         
        | 4177 instances
  - ID 25 | Slugs                            
        | 1060 instances
  - ID 26 | Snails                           
        | 1356 instances
  - ID 27 | Spider Mites                     
        | 2826 instances
  - ID 28 | Squash Powdery mildew leaf               | 314 instances
  - ID 29 | Tomato Early blight leaf         
        | 271 instances
  - ID 30 | Tomato Septoria leaf spot                | 523 instances
  - ID 31 | Tomato leaf                      
        | 604 instances
  - ID 32 | Tomato leaf bacterial spot               | 352 instances
  - ID 33 | Tomato leaf late blight          
        | 293 instances
  - ID 34 | Tomato leaf mosaic virus         
        | 326 instances
  - ID 35 | Tomato leaf yellow virus         
        | 955 instances
  - ID 36 | Tomato mold leaf                 
        | 326 instances
  - ID 37 | Tomato two spotted spider mites leaf     | 2 instances
  - ID 38 | Wasps                            
        | 1346 instances
  - ID 39 | Weevils                          
        | 1138 instances
  - ID 40 | Yellow Leaf Curl Virus           
        | 5343 instances
  - ID 41 | Yellow Rust                      
        | 56 instances
  - ID 42 | fire                             
        | 27060 instances
  - ID 43 | horse                            
        | 1866 instances
  - ID 44 | pig                              
        | 43106 instances
  - ID 45 | sheep                            
        | 17728 instances
  - ID 46 | smoke                            
        | 18506 instances
========================================     
PS C:\Users\HP\Desktop\opencvpython>


final5000400ones
rs/HP/Desktop/opencvpython/CLASS5000400.PY
Starting dataset filtering process...
Selected classes to keep: ['Ants', 'Bees', 'Beetles', 'Black Rust', 'Brown Rust', 'COW', 'Caterpillars', 'Early Blight', 'Earthworms', 'Grasshoppers', 'Healthy', 'Healthy Wheat', 'Potato leaf', 'Potato leaf early blight', 'Potato leaf late blight', 'Tomato Early blight leaf', 'Tomato Septoria leaf spot', 'Tomato leaf', 'Tomato leaf bacterial spot', 'Tomato leaf late blight', 'Tomato leaf mosaic virus', 'Tomato leaf yellow virus', 'Tomato mold leaf', 'Tomato two spotted spider mites leaf', 'fire', 'horse', 'person', 'pig', 'sheep', 'smoke']
Original indices: [0, 1, 2, 3, 4, 5, 6, 10, 11, 13, 14, 15, 21, 22, 23, 29, 30, 31, 32, 33, 34, 35, 36, 37, 42, 44, 45, 46, 47, 48]    
New index mapping (old_index -> new_index): {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 10: 7, 11: 8, 13: 9, 14: 10, 15: 11, 21: 12, 22: 13, 23: 14, 29: 15, 30: 16, 31: 17, 32: 18, 33: 19, 34: 20, 35: 21, 36: 22, 37: 23, 42: 24, 44: 25, 45: 26, 46: 27, 47: 28, 48: 29}   

Creating new dataset directory at: filtered_farm_safety_dataset5400

Processing 'train' split...
Original labels directory: C:/Users/HP/Desktop/ALLmaster_dataset/train/labels    
Finished processing 'train'. Copied 59685 images and their labels.

Processing 'val' split...  
Original labels directory: C:/Users/HP/Desktop/ALLmaster_dataset/valid/labels    
Finished processing 'val'. Copied 8253 images and their labels.

Processing 'test' split... 
Original labels directory: C:/Users/HP/Desktop/ALLmaster_dataset/test/labels     
Finished processing 'test'. Copied 4283 images and their labels.

Successfully created new dataset at 'filtered_farm_safety_dataset5400'
New configuration file saved at 'filtered_farm_safety_dataset5400\data.yaml'     

--- Starting Dataset Balancing for Training Set ---   
Initial class distribution (image count):
  - Ants: 1032 images
  - Bees: 1101 images      
  - Beetles: 857 images    
  - Black Rust: 21 images  
  - Brown Rust: 25 images  
  - COW: 8696 images       
  - Caterpillars: 912 images
  - Early Blight: 2067 images
  - Earthworms: 720 images 
  - Grasshoppers: 1044 images
  - Healthy: 756 images    
  - Healthy Wheat: 592 images
  - Potato leaf: 37 images 
  - Potato leaf early blight: 96 images
  - Potato leaf late blight: 85 images
  - Tomato Early blight leaf: 81 images
  - Tomato Septoria leaf spot: 121 images
  - Tomato leaf: 88 images 
  - Tomato leaf bacterial spot: 99 images
  - Tomato leaf late blight: 89 images
  - Tomato leaf mosaic virus: 51 images
  - Tomato leaf yellow virus: 65 images
  - Tomato mold leaf: 79 images
  - Tomato two spotted spider mites leaf: 1 images    
  - fire: 13894 images     
  - horse: 1480 images     
  - person: 3764 images    
  - pig: 5576 images       
  - sheep: 3683 images     
  - smoke: 13667 images    

--- Starting Undersampling ---
Undersampling class 'COW': removing 3696 of 8696 images.
Undersampling class 'fire': removing 8894 of 13894 images.
Undersampling class 'pig': removing 576 of 5576 images.
Undersampling class 'smoke': removing 8667 of 13667 images.

Rescanning dataset after undersampling...
Class distribution after undersampling:
  - Ants: 1032 images
  - Bees: 1101 images      
  - Beetles: 857 images    
  - Black Rust: 21 images  
  - Brown Rust: 25 images  
  - COW: 5000 images       
  - Caterpillars: 912 images
  - Early Blight: 2067 images
  - Earthworms: 720 images 
  - Grasshoppers: 1044 images
  - Healthy: 756 images    
  - Healthy Wheat: 592 images
  - Potato leaf: 37 images 
  - Potato leaf early blight: 96 images
  - Potato leaf late blight: 85 images
  - Tomato Early blight leaf: 81 images
  - Tomato Septoria leaf spot: 121 images
  - Tomato leaf: 88 images 
  - Tomato leaf bacterial spot: 99 images
  - Tomato leaf late blight: 89 images
  - Tomato leaf mosaic virus: 51 images
  - Tomato leaf yellow virus: 65 images
  - Tomato mold leaf: 79 images
  - Tomato two spotted spider mites leaf: 1 images    
  - fire: 4798 images      
  - horse: 1480 images     
  - person: 3764 images    
  - pig: 5000 images       
  - sheep: 3683 images     
  - smoke: 4801 images     

--- Starting Oversampling (by duplication) ---        
Oversampling class 'Black Rust': adding 379 images to reach 400.
Oversampling class 'Brown Rust': adding 375 images to reach 400.
Oversampling class 'Potato leaf': adding 363 images to reach 400.
Oversampling class 'Potato leaf early blight': adding 304 images to reach 400.   
Oversampling class 'Potato leaf late blight': adding 315 images to reach 400.    
Oversampling class 'Tomato Early blight leaf': adding 319 images to reach 400.   
Oversampling class 'Tomato Septoria leaf spot': adding 279 images to reach 400.  
Oversampling class 'Tomato leaf': adding 312 images to reach 400.
Oversampling class 'Tomato leaf bacterial spot': adding 301 images to reach 400. 
Oversampling class 'Tomato leaf late blight': adding 311 images to reach 400.    
Oversampling class 'Tomato leaf mosaic virus': adding 349 images to reach 400.   
Oversampling class 'Tomato leaf yellow virus': adding 335 images to reach 400.   
Oversampling class 'Tomato mold leaf': adding 321 images to reach 400.
Oversampling class 'Tomato two spotted spider mites leaf': adding 399 images to reach 400.

--- Balancing Complete --- 
Final class distribution in 'train' set:
  - Ants: 1032 images
  - Bees: 1101 images      
  - Beetles: 857 images    
  - Black Rust: 420 images 
  - Brown Rust: 417 images 
  - COW: 5000 images       
  - Caterpillars: 912 images
  - Early Blight: 2067 images
  - Earthworms: 720 images 
  - Grasshoppers: 1044 images
  - Healthy: 756 images    
  - Healthy Wheat: 861 images
  - Potato leaf: 549 images
  - Potato leaf early blight: 507 images
  - Potato leaf late blight: 674 images
  - Tomato Early blight leaf: 832 images
  - Tomato Septoria leaf spot: 411 images
  - Tomato leaf: 535 images
  - Tomato leaf bacterial spot: 802 images
  - Tomato leaf late blight: 447 images
  - Tomato leaf mosaic virus: 410 images
  - Tomato leaf yellow virus: 428 images
  - Tomato mold leaf: 406 images
  - Tomato two spotted spider mites leaf: 400 images  
  - fire: 4798 images      
  - horse: 1480 images     
  - person: 3764 images    
  - pig: 5000 images       
  - sheep: 3683 images     
  - smoke: 4801 images     
PS C:\Users\HP\Desktop\opencvpython>
