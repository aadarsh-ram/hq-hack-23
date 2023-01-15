import React, { useRef, useState } from "react";
import styles from './Upload.module.css'
import img from '../../../public/assets/Uploadimg.png'
import { Button, IconButton } from "@mui/material";
import { UploadFile } from "@mui/icons-material";
import { Apiurls } from "../../utils/content";
import ResultsPage from "../ResultsPage/ResultsPage";

const Upload = () => {
	const [isFilePicked, setIsFilePicked] = useState(false);
    const input = useRef<HTMLInputElement>(null);

    const handleclick = ()=>{
        if(input!=null){
            input.current?.click();
        }
    }

    const handleupload = (event : React.ChangeEvent<HTMLInputElement>)=>{
        if(event.target.files!=null){
            let uploadedFile:File = event.target.files[0];
            const file = new FormData();
		    file.append('file', uploadedFile);
            fetch(Apiurls[0].url,
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
            setIsFilePicked(true)
        }
    }

    return (
        !isFilePicked? <div className={styles.upload}>
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
        </div>: <ResultsPage />
    );
}
 
export default Upload;