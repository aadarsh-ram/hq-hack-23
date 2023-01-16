import { Button, Dialog, Typography} from "@mui/material";
import * as React from "react"
import styles from "./ViewUploads.module.css"
import { Apiurls } from "../../utils/content";
import { redirect, useNavigate } from "react-router-dom";



type modalProps = {
    open:boolean,
    handleClose :() => void,
    content : string,
}



const ViewUploads = () => {

    type jd={
        id:number,
        jdContent:string,
        keywords:string,
    }

    const navigate = useNavigate();


    const[alljds,setAlljds] = React.useState<jd[]>([])
    const[fetchedjds,setFetchedjds]=React.useState<boolean>(false);
    const [open,setOpen] = React.useState<boolean>(false);
    const[jdcontent,setJdcontent] = React.useState<string>('');
    const[jdid,setJdid] = React.useState<number>(0);

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
                <Button onClick={handleredirect}>
                    Perform this search
                </Button>
            </Dialog>
        )
    }

    const handleredirect = ()=>{
        navigate(`/results/${jdid}`,{replace:true})
    }

    const handleclose = ()=>{
        setOpen(false)
    }

    const handleClick=(index:number)=>{
        setJdcontent(alljds[index].jdContent);
        setOpen(true)
        setJdid(index)
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
            res.forEach((ele:any)=>{
                const newele:jd ={
                    id:ele.id,
                    jdContent:ele.jd_content,
                    keywords:ele.keywords
                }
                setAlljds((alljds)=>[...alljds,newele])
            })
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
                <Typography variant="h4">
                    My Uploads
                </Typography>
            </div>
            {fetchedjds? <div className={styles.uploads}>
                    {
                        alljds.map((ele,index)=>{
                            return(
                                <div className={styles.uploaditem}>
                                    <div>
                                        Upload No {ele.id}
                                    </div>
                                    <Button onClick={()=>handleClick(index)}>
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