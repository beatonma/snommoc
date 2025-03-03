export const Age = (props: { age: number }) => {
  const { age } = props;
  if (!age) return null;

  return <span>{age} years</span>;
};
