/* Copyright (c) 2022 Pixel Flux
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#include "entity.hpp"

#include <stdexcept>

using namespace pyflecs;

entity::entity(ecs_world_t* world, const ecs_entity_t e) :
    mpWorld(world),
    mRaw(e)
{
}

entity::~entity()
{

}


bulk_entity_builder::bulk_entity_builder(ecs_world_t* pWorld, int32_t count) : 
    mpWorld(pWorld),
    mDesc{}
{

}

void bulk_entity_builder::add(ecs_id_t eid, void* data)
{

    mDesc.ids[mData.size()] = eid;
    mData.push_back(data);
}

std::vector<pyflecs::entity> bulk_entity_builder::build()
{
    mDesc.data = mData.data();
    auto result = ecs_bulk_init(mpWorld, &mDesc);
    if (result == nullptr)
        throw std::runtime_error("Error on bulk creation with ID");
    std::vector<pyflecs::entity> entities;
    for (int32_t idx = 0; idx < mDesc.count; idx++)
    {
        entities.push_back(pyflecs::entity(mpWorld, result[idx]));
    }
    return entities;
}