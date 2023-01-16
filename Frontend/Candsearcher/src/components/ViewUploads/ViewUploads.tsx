import { Button, Dialog} from "@mui/material";
import * as React from "react"
import styles from "./ViewUploads.module.css"
import { Apiurls } from "../../utils/content";


type modalProps = {
    open:boolean,
    handleClose :() => void,
    content : string,
}


const Modal = (props:modalProps) =>{
    return(
        <Dialog 
        open={props.open}
        onClose={props.handleClose}
        className={styles.modal}
        >
            <div className={styles.content}>
                {props.content}
            </div>
            <Button>
                Perform this search
            </Button>
        </Dialog>
    )
}


const ViewUploads = () => {

    type jd={
        id:number,
        jdContent:string,
        keywords:string,
    }


    const [alljds,setAlljds] = React.useState<jd[]>([]);
    const[fetchedjds,setFetchedjds]=React.useState<boolean>(false);
    const [open,setOpen] = React.useState<boolean>(false);
    const[jdcontent,setJdcontent] = React.useState<string>('');

    const handleclose = ()=>{
        setOpen(false)
    }

    const handleClick=()=>{

    }

    React.useEffect(()=>{
        fetch(Apiurls[1].url,
            {
                method: 'GET',
                headers:{
                    'accept':'application/json'
                }
            }
        ).then(async(response)=>{
            let res = await response.json()
            setAlljds(res)
            setFetchedjds(true)
        }).catch((error)=>{
            console.log(error);
        })
    },[])

    const view=[1,2,3,4]

    return ( 
        <div className={styles.container}>
            <Modal open={open} handleClose={handleclose} content={jdcontent} />
            <div className={styles.title}>
                My Uploads
            </div>
            {fetchedjds? <div className={styles.uploads}>
                    {
                        alljds.map((ele)=>{
                            return(
                                <div className={styles.uploaditem}>
                                    <div>
                                        Upload No {ele.id}
                                    </div>
                                    <Button onClick={handleClick}>
                                        Show More
                                    </Button>
                                </div>
                            )
                        })
                    }
                </div>:<></>
            }
        </div>
    );
}
 
export default ViewUploads;