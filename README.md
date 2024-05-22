# escootersim  
  
## 1. High-Level Documentation for Each Folder 
  



├── Experiment: *main folder we use for the experiment.*  
│   ├── controller: *scripts for ESP32. Open this folder for uploading app to ESP32.*   
│   │   ├── _old  
│   │   ├── data  
│   │   ├── include  
│   │   ├── lib  
│   │   ├── src: *main folder for cpp codes*  
│   │   └── test  
│   └── server: scripts for host  
│       ├── audio: *all audio data is here*  
│       ├── node_modules  
│       ├── public  
│           ├── index.html: home page  
│           └── spotify.html: *spotyfy authorization page*  
├── Unity_essim: *for unity environment(escooter base only)*  
├── _old: *don't use this folder anymore*  
├── micon  
│   ├── arduino: *don't use this folder anymore*  
│   │   ├── sketch_mar29a  
│   │   └── unity_test  
│   ├── circuit_playground: *don't use this folder anymore*  
│   └── escootersim_pypico: *scripts for getting AC, BR, ST data from the escooter*  
│       ├── include  
│       ├── lib  
│       ├── src  
│       └── test  
├── prototyping: *for documenting prototypes*  
│   └── asset  
│       └── img: *GIF is git-ignored*  
└── videos: *videos from our pilot experiment(must be git-ignored)*  
  


## 2. Compile Instructions

### 2-1. Upload code to ESP32

1. Let's start from "3. Install PlatformIO on Visual Studio Code" in this page  https://github.com/rye-m/tiltybot_workshop/wiki/01_Prep_%E4%BA%8B%E5%89%8D%E6%BA%96%E5%82%99

2. And then, follow the instruction at https://github.com/rye-m/tiltybot_workshop/wiki/02_Instruction_%E3%83%99%E3%83%BC%E3%82%B9%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88%E3%81%AE%E4%BD%9C%E3%82%8A%E6%96%B9

### 2-2. Hosting webserver in your laptop

1. go to `cd escootersim/Experiment/server`  
2. `npm init`
3. `npm start` 

