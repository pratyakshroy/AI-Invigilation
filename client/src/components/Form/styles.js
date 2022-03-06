
import { makeStyles } from '@material-ui/core/styles';

export default makeStyles((theme) => ({
  root: {
    Color: '#daa520',
    
     
    '& .MuiTextField-root': {
      margin: theme.spacing(0),
    },
  },
  paper: {
    
    
    backgroundColor: '#aebec9d5',
    padding: theme.spacing(2),
  },
  form: {
    color: '#FFD700',
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
  },
  
  buttonSubmit: {
    
    backgroundColor: '#daa520',
    marginBottom: 10,
  },
}));
