from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.vacancy import Vacancy
from src.db.models.user import User
from src.db.session import async_engine
from src.vacancy.schemas import VacancyModel
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import select 
from sqlalchemy.orm.attributes import flag_modified
from src.user.router import current_user

router_vacancy = APIRouter()


@router_vacancy.get("/")
async def create_vacancy(vacancy: VacancyModel, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session: 
        query = select(Vacancy)
        result = await session.execute(query)
        events = result.scalars().all()

        return events
    
# @router_vacancy.
#     # async with AsyncSession(async_engine) as session:
#     #     user = await session.get(User, user.id)



#         # if user.role_id == 3:
#         #     new_vacancy = Vacancy(
#         #         vacancy_name=vacancy.vacancy_name,
#         #         description=vacancy.description,
#         #         amount=vacancy.amount,
#         #         company=vacancy.company
#         #     )
        
#         #     session.add(new_vacancy)
#         #     await session.commit()
#         #     await session.refresh(new_vacancy)
        
#         #     return {
#         #         "message": "The event has been created: "
#         #         }, new_event
#         #     return {"message": "Insufficient permissions to create events."}
    

# @router_events.get("/events/get-event/{event_id}")
# async def get_event(event_id: int):
#     async with AsyncSession(async_engine) as session:
#         event = await session.get(Event, event_id)

#         if not event:
#             raise HTTPException(status_code=404, detail=f"Event {event_id} is not found.")
        
#         return {"message": f"The event {event_id}: "}, event


# @router_events.put("/events/get-event/{event_id}/edit-event")
# async def edit_event(event_id: int, new_event: EventModel, user: User = Depends(current_user)):
#     async with AsyncSession(async_engine) as session:
#         user = await session.get(User, user.id)

#         if user.role_id == 1:
#             event = await session.get(Event, event_id)

#             if not event:
#                 raise HTTPException(status_code=404, detail="Event is not found.")
        
#             event.title = new_event.title
#             event.description = new_event.description
#             event.date = new_event.date
#             event.organizer = new_event.organizer

#             await session.commit()
#             await session.refresh(event)
        
#             return {"message": "The event has been edited: "}, event
#         else:
#             return {"message": "Insufficient permissions to edit event."}
    

# @router_events.delete("/events/get-event/{event_id}/delete-event")
# async def delete_event(event_id: int, user: User = Depends(current_user)):
#     async with AsyncSession(async_engine) as session:
#         user = await session.get(User, user.id)

#         if user.role_id == 1:
#             event = await session.get(Event, event_id)

#             if not event:
#                 raise HTTPException(status_code=404, detail="Event is not found.")

#             query = select(User)
#             result = await session.execute(query)
#             users = result.scalars().all()

#             await delete_event_from_users(event_id, users)
       
#             await session.delete(event)
#             await session.commit()

#             query = select(Event)
#             result = await session.execute(query)
#             events = result.scalars().all()

#             return {"message": "The event has been deleted: "}, events
#         else:
#             return {"message": "Insufficient permissions to delete events."}
    

# async def delete_event_from_users(event_id, users):
#     for user in users:
#         if event_id in user.events:
#             user.events.remove(event_id)
#             flag_modified(user, "events")


# @router_events.get("/events/get-event/{even_id}/get-performers")
# async def get_performers(event_id: int):
#     async with AsyncSession(async_engine) as session:
#         event = await session.get(Event, event_id)

#         if not event:
#             raise HTTPException(status_code=404, detail="Event is not found.")
        
#         query = select(User)
#         result = await session.execute(query)
#         users = result.scalars().all()

#         target_users = []

#         for user in users:
#             if event_id in user.events:
#                 target_users.append(user)

#         return {"message": f"Participants of the event {event_id}: "}, target_users


# @router_events.get("/events/get-event/{even_id}/get-organizer")
# async def get_organizer(event_id: int):
#     async with AsyncSession(async_engine) as session:
#         event = await session.get(Event, event_id)

#         if not event:
#             raise HTTPException(status_code=404, detail="Event is not found.")
        
#         user_id = event.organizer
#         user = await session.get(User, user_id)

#         if not user:
#             raise HTTPException(status_code=404, detail="User is not found.")

#         return {"message": f"The organizer of event {event_id}: "}, user
    

# @router_events.get("/events/get-all-events")
# async def get_all_events():
#     async with AsyncSession(async_engine) as session: 
#         query = select(Event)
#         result = await session.execute(query)
#         events = result.scalars().all()

#         return {"message": "List of all events: "}, events
    

# @router_events.put("/{user_id}/events/add-event/{event_id}")
# async def add_event_to_user(event_id: int, user: User = Depends(current_user)):
#     async with AsyncSession(async_engine) as session:
#         user = await session.get(User, user.id)

#         event = await session.get(Event, event_id)

#         if not event:
#             raise HTTPException(status_code=404, detail="Event is not found.")

#         if event_id not in user.events:
#             user.events.append(event_id)
#             event.performers.append(user.id)
#             flag_modified(event, "performers")
#             flag_modified(user, "events")
#         else:
#             return {"message": "Event has already been added: "}, user

#         await session.commit()
#         await session.refresh(user)

#         return {"message": "The event has been added: "}, user
    

# @router_events.delete("/{user_id}/events/get-event/delete-event/{event_id}")
# async def delete_event_from_user(event_id: int, user: User = Depends(current_user)):
#     async with AsyncSession(async_engine) as session:
#         user = await session.get(User, user.id)
        
#         event = await session.get(Event, event_id)

#         if not event:
#             raise HTTPException(status_code=404, detail="Event is not found.")

#         if event_id in user.events:
#             user.events.remove(event_id)
#             event.performers.remove(user.id)
#             flag_modified(event, "performers")
#             flag_modified(user, "events")
#         else:
#             return {"message": "User does not have this event."}, user

#         await session.commit()
#         await session.refresh(user)

#         return {"message": "The event has been deleted: "}, user
    

# @router_events.get("/{user_id}/events/get-events")
# async def get_events_from_user(user: User = Depends(current_user)):
#     async with AsyncSession(async_engine) as session:
#         user = await session.get(User, user.id)
        
#         query = select(Event)
#         result = await session.execute(query)
#         events = result.scalars().all()

#         target_events = []

#         for event in events:
#             if event.id in user.events:
#                 target_events.append(event)

#         return {"message": "User`s events: "}, target_events
    

# @router_events.get("/{user_id}/events/get-event/{event_id}")
# async def get_event_from_user(event_id: int, user: User = Depends(current_user)):
#     async with AsyncSession(async_engine) as session:
#         user = await session.get(User, user.id)

#         event = await session.get(Event, event_id)

#         if not event:
#             raise HTTPException(status_code=404, detail="Event is not found.")

#         if event_id in user.events: 
#             return True
#         else:
#             return False
