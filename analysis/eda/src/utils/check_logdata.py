import marimo

__generated_with = "0.8.7"
app = marimo.App(width="medium")


@app.cell
def __():
    import os

    prefix = "CSV_Scenario-"
    folder_counter = 0

    def passer():
        pass

    def check_file_name(file_path):
        # Get the file name from the path
        file_name = os.path.basename(file_path)

        # Check if the file name starts with the specified characters
        for filename in filename_list:
            if file_name.startswith(prefix + filename):
                filename_list.remove(filename)
                return True

        return False, file_name

    if __name__ == "__main__":
        
        # Get file path from the user
        folder_path = "/Users/ryem/Desktop/Cornell_Tech/escootersim/analysis/eda/Data/"
        folders_temp = os.listdir(folder_path)
        folders = []
        for item in folders_temp:
            if item.startswith("P"):
                folders.append(item)
        print(folders)
        
        for folder in folders:
            print(folder)
            file_counter = 0
            folder_counter +=1
            filename_list = ["ScooterStudyenv", "Nback_Button", "Nback_Footbutton", "Nback_Phone", "Nback_Voice", "Nback_Throttle", "Nback_Watch", "Song_Button", "Song_Footbutton", "Song_Phone", "Song_Voice", "Song_Throttle", "Song_Watch"]

        
            files = os.listdir(folder_path + "/" + folder)
            for file in files:
                # Validate the file path
                if os.path.isfile(folder_path + "/" + folder + "/" + file):
            
                    result = check_file_name(folder_path + "/" + file)
            
                    if result is True:
                        # print("The file name is correct.")
                        file_counter+=1
                    else:
                        print(f"Unmatched file name: {result[1]}")
            print("\tTotal file number: " + str(file_counter))
            print("\tThe list: ", filename_list)
        print("folder_counter:", folder_counter)
    return (
        check_file_name,
        file,
        file_counter,
        filename_list,
        files,
        folder,
        folder_counter,
        folder_path,
        folders,
        folders_temp,
        item,
        os,
        passer,
        prefix,
        result,
    )


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
