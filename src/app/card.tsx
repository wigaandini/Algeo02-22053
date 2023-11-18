interface CardProps {
  image: string;
  similarity: number;
}

const Card: React.FC<CardProps> = ({ image, similarity }) => {
  return (
    <div className="card">
      <img src={image} className="card-image" alt="Uploaded Image" />
      <div className="card-overlay">
        <p className="similarity-text">Similarity: {similarity.toFixed(4)} %</p>
      </div>

      <style jsx>{`
        .card {
          position: relative;
          width: 300px; /* Set your desired width */
          height: 300px; /* Set your desired height */
          overflow: hidden;
          border-radius: 8px;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
          margin: 16px;
        }

        .card-image {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .card-overlay {
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          background: rgba(0, 0, 0, 0.7);
          padding: 8px;
          text-align: center;
          color: #fff;
        }

        .similarity-text {
          margin: 0;
        }
      `}</style>
    </div>
  );
};

export default Card;
