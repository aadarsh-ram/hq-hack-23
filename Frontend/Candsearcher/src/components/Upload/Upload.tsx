import React, { useRef, useState } from "react";
import styles from './Upload.module.css'
import img from '../../../public/assets/Uploadimg.png'
import { Button, IconButton } from "@mui/material";
import { UploadFile } from "@mui/icons-material";
// import uploadIcon from '../../../public/assets/uploadIcon.png'

const Upload = () => {

    // const[isSelected,setIsSelected] = useState(false);
    // const [selectedFile, setSelectedFile] = useState<any>(null);
	const [isFilePicked, setIsFilePicked] = useState(false);

    // let file : File = undefined
    const input = useRef<HTMLInputElement>(null);

    const handleclick = ()=>{
        if(input!=null){
            input.current?.click();
        }
    }

    const handleupload = (event : React.ChangeEvent<HTMLInputElement>)=>{
        console.log("gg");
        console.log(event.target.files)
        if(event.target.files!=null){
            setIsFilePicked(true)
            let Fileeee:File = event.target.files[0];
            const file = new FormData();
		    file.append('file', Fileeee);
            fetch("http://localhost:8000/candidate-profiles/uploadpdf",
                {
				    method: 'POST',
                    body:file,
			    }
            ).then((response)=>{
                console.log(response.body);
            })
            .catch((error)=>{
                console.log(error);
            })
        }
    }

    return (
        <div className={styles.upload}>
            <input
                accept="application/pdf"
                style={{ display: 'none' }}
                type="file"
                hidden
                ref={input}
                onChange={handleupload}
            />
            <div className={styles.uploadBox}>
                <img src={img}>
                </img>
                <div className={styles.buttondiv}>
                    <Button endIcon={<UploadFile />} className={styles.uploadbtn} onClick={handleclick}>
                        Upload
                    </Button>
                </div>
            </div>
        </div>
    );
}
 
export default Upload;