import { useQuery } from 'react-query';

interface Cat {
    _id: string;
    text: string;
}

interface Props {
    className?: string;
}

export default function Cats({ className }: Props) {
    const { data, error, isLoading } = useQuery<Cat[]>('cats', () => fetch('/cats.json').then((res) => res.json()));

    if (isLoading) return <>Loading...</>;

    if (error) {
        return <>An error has occurred</>;
    }

    // eslint-disable-next-line no-underscore-dangle
    return <ul className={className}>{data && data.map((cat) => <li key={cat._id}>{cat.text}</li>)}</ul>;
}
