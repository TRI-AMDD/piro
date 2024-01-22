// FeedbackButton.tsx

import React from 'react';
import { Button } from '@material-tailwind/react';
import styles from './components.module.css';

interface FeedbackButtonProps {
  showFeedbackButton: boolean;
}

const customStyles = {
              verticalAlign: "align-middle",
              textTransform: "lowercase",

  };

const FeedbackButton: React.FC<FeedbackButtonProps> = () => {
  // Add your feedback button logic here
  return (
    <div className="absolute top-20 right-0 h-full flex items-center p-0 transform rotate-90">
        <Button variant="filled" className={styles.FeedbackButton} onClick={()=>window.showCollectorDialog()}>
             Feedback
        </Button>
    </div>
  )
};

export default FeedbackButton;
