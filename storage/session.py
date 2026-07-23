user_sessions = {}


def set_current_premise(
    user_id,
    index
):

    user_sessions[str(user_id)] = index



def get_current_premise(
    user_id
):

    return user_sessions.get(
        str(user_id),
        0
    )