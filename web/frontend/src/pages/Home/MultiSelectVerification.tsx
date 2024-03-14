import CreatableSelect from 'react-select/creatable';
import { MultiValue } from 'react-select';
import styles from './Home.module.css';
import { Optionselect } from './TypeProps';
import { Dispatch, SetStateAction } from 'react';
import { CSSObject } from '@emotion/react';
import { useState } from 'react';
const customStyles = {
  control: (base: CSSObject) => ({
    ...base,
    borderColor: '#757575',
    borderWidth: '1px',
    boxShadow: '0 0 0 1px white',
    '&:hover': {
      borderColor: '#212121',
      boxShadow: '0 0 0 1px black'
    }
  })
};

interface Props {
  placeholder?: string;
  setValues: Dispatch<SetStateAction<MultiValue<Optionselect>>>;
}
interface Option {
    value: string;
    label: string;
  }
  const elements = [
    "H","He",
    "Li","Be","B","C","N","O","F","Ne",
    "Na","Mg","Al","Si","P","S","Cl","Ar",
    "K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr",
    "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe",
    "Cs","Ba","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn",
    "Fr","Ra","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og",
    "La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu",
    "Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr",
    "h","he",
    "li","be","b","c","n","o","f","ne",
    "na","mg","al","si","p","s","cl","ar",
    "k","ca","sc","ti","v","cr","mn","fe","co","ni","cu","zn","ga","ge","as","se","br","kr",
    "rb","sr","y","zr","nb","mo","tc","ru","rh","pd","ag","cd","in","sn","sb","te","i","xe",
    "cs","ba","hf","ta","w","re","os","ir","pt","au","hg","tl","pb","bi","po","at","rn",
    "fr","ra","rf","db","sg","bh","hs","mt","ds","rg","cn","nh","fl","mc","lv","ts","og",
    "la","ce","pr","nd","pm","sm","eu","gd","tb","dy","ho","er","tm","yb","lu",
    "ac","th","pa","u","np","pu","am","cm","bk","cf","es","fm","md","no","lr",
    "h","hE",
    "lI","bE","b","c","n","o","f","nE",
    "nA","mG","aL","sI","p","s","cL","aR",
    "k","cA","sC","tI","v","cR","mN","fE","cO","nI","cU","zN","gA","gE","aS","sE","bR","kR",
    "rB","sR","y","zR","nB","mO","tC","rU","rH","pD","aG","cD","iN","sN","sB","tE","i","xE",
    "cS","bA","hF","tA","w","rE","oS","iR","pT","aU","hG","tL","pB","bI","pO","aT","rN",
    "fR","rA","rF","dB","sG","bH","hS","mT","dS","rG","cN","nH","fL","mC","lV","tS","oG",
    "lA","cE","pR","nD","pM","sM","eU","gD","tB","dY","hO","eR","tM","yB","lU",
    "aC","tH","pA","u","nP","pU","aM","cM","bK","cF","eS","fM","mD","nO","lR",
    "H","HE",
    "LI","BE","B","C","N","O","F","NE",
    "NA","MG","AL","SI","P","S","CL","AR",
    "K","CA","SC","TI","V","CR","MN","FE","CO","NI","CU","ZN","GA","GE","AS","SE","BR","KR",
    "RB","SR","Y","ZR","NB","MO","TC","RU","RH","PD","AG","CD","IN","SN","SB","TE","I","XE",
    "CS","BA","HF","TA","W","RE","OS","IR","PT","AU","HG","TL","PB","BI","PO","AT","RN",
    "FR","RA","RF","DB","SG","BH","HS","MT","DS","RG","CN","NH","FL","MC","LV","TS","OG",
    "LA","CE","PR","ND","PM","SM","EU","GD","TB","DY","HO","ER","TM","YB","LU",
    "AC","TH","PA","U","NP","PU","AM","CM","BK","CF","ES","FM","MD","NO","LR"
  ];
const options: Option[] = elements.map(element => ({ value: element, label: element }));

export default function MultiSelectVerification(props: Props) {
    const [error, setError] = useState<string>('');
    const handleInputChange = (inputValue: string) => {
        if (!inputValue) {
          setError('');
          return;
        }
    
        if (!options.find((option) => option.value.toLowerCase() === inputValue.toLowerCase()))
 {
          setError('Enter a correct chemical symbol');
        } else {
          setError('');
        }
      }; 
  const { placeholder, setValues } = props;
  const emptyOptions: Optionselect[] = [];
  return (
    <div className={styles.Multi}>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      <CreatableSelect
        isValidNewOption={(inputValue) =>
            options.find((option) => option.value === inputValue) ? true : false
        }
        onInputChange={handleInputChange}
        styles={customStyles}
        placeholder={placeholder}
        isMulti
        onChange={(newValues) => setValues(newValues)}
        options={emptyOptions}
        className={styles.custumcreateselect}
      />
    </div>
  );
}
