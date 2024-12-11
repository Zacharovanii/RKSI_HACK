from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import async_engine
from src.user.router import current_user

from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import select

from src.projects.schemas import ProjectCreateModel, ProjectReadModel, ProjectEditModel
from src.db.models.project import Project
from src.db.models.user import User

router_project = APIRouter()


@router_project.get("/",  response_model=List[ProjectReadModel])
async def get_all_projects() -> List[ProjectReadModel]:
    async with AsyncSession(async_engine) as session: 
        query = select(Project)
        result = await session.execute(query)
        projects = result.scalars().all()

        return projects
    

@router_project.get("/{id}",  response_model=ProjectReadModel)
async def get_project(id: int) -> ProjectReadModel:
    async with AsyncSession(async_engine) as session:
        project = await session.get(Project, id)

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )
        
        return project
    

@router_project.get("/user/{id}",  response_model=List[ProjectReadModel])
async def get_all_user_projects(id: int) -> List[ProjectReadModel]:
    async with AsyncSession(async_engine) as session:
        query = select(Project).filter(Project.owner==id)
        result = await session.execute(query)
        projects = result.scalars().all()

        return projects
    

@router_project.post("/add")
async def create_project(project: ProjectCreateModel, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        new_project = Project(
            title=project.title,
            description=project.description,
            file_link=project.file_link
        )

        new_project.owner = user.id
        new_project.created_at = datetime.now()
        
        session.add(new_project)
        user.projects.append(new_project.title)
        flag_modified(user, "projects")
        await session.commit()

        return {
            "message": "The project has been added successfully"
        }


@router_project.put("/{id}/edit")
async def edit_project(id: int, new_project: ProjectEditModel, user: User = Depends(current_user)):
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)
        project = await session.get(Project, id)

        if user.role_id == 4 or user.id == 1:
            if project:
                if user.id == project.owner:
                    user.projects.remove(project.title)
                    
                    project.title = new_project.title
                    project.description = new_project.description
                    project.file_link=new_project.file_link

                    user.projects.append(project.title)
                    flag_modified(user, "projects")
                    await session.commit()

                    return {
                        "message": "The project has been edited successfully"
                    }
                else:
                    raise HTTPException(
                    status_code=403,
                        detail="Only the owner and admin can edit projects"
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Project not found"
                )
        else:
            raise HTTPException(
                status_code=403,
                detail="Insufficient rights to edit projects"
            )
            

@router_project.delete("/delete")
async def delete_all_projects(user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id == 4:
            query = select(Project)
            result = await session.execute(query)
            projects = result.scalars().all()

            for project in projects:
                await session.delete(project)
                await session.commit()

            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()

            for user in users:
                user.projects.clear
                flag_modified(user, "projects")
                await session.commit()

            return {
                "message": "All projects have been deleted successfully"
            }
        else:
            raise HTTPException(
                    status_code=403,
                    detail="Insufficient rights to delete projects"
                )
    

@router_project.delete("/{id}/delete")
async def delete_vacancy(id: int, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)
        project = await session.get(Project, id)

        if user.role_id == 1 or user.role_id == 4:
            if project:
                if user.id == project.owner:
                    user.projects.remove(project.title)
                    flag_modified(user, 'projects')
                    await session.delete(project)
                    await session.commit()

                    return {
                        "message": "The project has been deleted successfully"
                    }
                else:
                    raise HTTPException(
                        status_code=403,
                        detail="Only the owner and admin can delete projects"
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Project not found"
                )
        else:
            raise HTTPException(
                status_code=404,
                detail="Insufficient rights to delete projects"
            )
        

@router_project.delete("/user/{id}/delete")
async def delete_user_project(id: int, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        target_user = await session.get(User, id)
        current_user = await session.get(User, user.id)

        if current_user.role_id == 4:
            query = select(Project).filter(Project.owner==id)
            result = await session.execute(query)
            projects = result.scalars().all()

            for project in projects:
                session.delete(project)

            target_user.projects.clear()
            flag_modified(target_user, "projects")

            await session.commit()

            return {
                "message": "All user`s projects have been dalatad successfully"
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="Insufficient rights to delete projects"
            )
