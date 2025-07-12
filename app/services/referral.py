from sqlalchemy.exc import SQLAlchemyError
from app.utils.database import get_session, init_db
from app.utils.database import User, Referral

# Initialize the database engine once
engine = init_db()

def add_user(user_id, username, invited_by=None):
    session = get_session(engine)
    try:
        # Create the user if not exists
        user = session.query(User).get(user_id)
        if not user:
            user = User(user_id=user_id, username=username)
            session.add(user)
            session.commit()
        
        # If invited_by is provided, record the referral
        if invited_by:
            # Check if the referrer exists
            referrer = session.query(User).get(invited_by)
            if referrer:
                # Record the referral
                referral = Referral(referrer_id=invited_by, referred_id=user_id)
                session.add(referral)
                # Update referrer's count
                referrer.referral_count = session.query(Referral).filter_by(referrer_id=invited_by).count()
                session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_referral_count(user_id):
    session = get_session(engine)
    try:
        user = session.query(User).get(user_id)
        if user:
            return user.referral_count
        return 0
    finally:
        session.close()
